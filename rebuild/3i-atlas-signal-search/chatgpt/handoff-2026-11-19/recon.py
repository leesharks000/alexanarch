from views import *
import hashlib
import urllib.request
import numpy as np
from scipy import fft

RAW_ROOT = "https://bldata.berkeley.edu/ATLAS/GB_ATLAS_raw/"

SMJD = {
    13: 17226, 14: 17543, 15: 17861,
    16: 18179, 17: 18497, 18: 18814,
}

FIRST_D19_BLOCK_SHA256 = {
    13: "bca4d54ed4008a646c9c7d1735f2dbe433f1678722132f4658baf81bdbe0d899",
    14: "0b58a5f78b9ac272f56c81b9392314f14c142bf1970d5d5c561b8a9ec7889930",
    15: "715962ce43ac6476fb18ca5cabaa9e14daa611a4fe67b59f9f859986112fcb49",
    16: "68e305dc9ce1e7da2614c2e654b1e7b628b2a44a4465f2639cfdb3d40eb38129",
    17: "db21aa987905d991a545af018e9e02c5d2b895a8bcfd17e9eb7e988e1fc90963",
    18: "d1acf0056e4f07efb2909ec4ad7199e35750eb1823769bced8157bfc10f256a8",
}

def fetch_channel_block(scan, block):
    file_index, local_block = divmod(block, 128)
    name = (
        f"blc23_guppi_61027_{SMJD[scan]}_DIAG_3I_ATLAS_"
        f"{scan:04d}.{file_index:04d}.raw"
    )
    count = 2097152
    start = local_block * 134224896 + 7168 + 7 * count
    stop = start + count - 1

    req = urllib.request.Request(
        RAW_ROOT + name,
        headers={"Range": f"bytes={start}-{stop}"}
    )

    with urllib.request.urlopen(req, timeout=60) as response:
        # Refuse a full-file fallback.
        assert response.status == 206
        assert response.headers["Content-Range"].startswith(
            f"bytes {start}-{stop}/"
        )
        payload = response.read(count + 1)

    assert len(payload) == count
    if block == 1634:
        assert hashlib.sha256(payload).hexdigest() == (
            FIRST_D19_BLOCK_SHA256[scan]
        )
    return payload

def reconstruct_d19(scan=13, first_block=1634):
    N = 1048576
    M = 4096
    center = 63733
    x = np.empty((2, 16384), dtype=np.complex64)

    for frame in range(4):
        pieces = [
            np.frombuffer(
                fetch_channel_block(scan, first_block + 2*frame + j),
                dtype=np.int8
            ).reshape(-1, 4)
            for j in [0, 1]
        ]
        raw = (
            np.maximum(np.concatenate(pieces).astype(np.float32), -127)
            / np.float32(127)
        )

        for feed in [0, 1]:
            v = raw[:, 2*feed] + 1j*raw[:, 2*feed + 1]
            X = fft.fftshift(fft.fft(v))
            selected = X[center-M//2:center+M//2]
            y = fft.ifft(fft.ifftshift(selected)) * np.float32(M/N)
            x[feed, frame*M:(frame+1)*M] = y

    # Match the original search's power-product precision:
    P = voltage_power(x.astype(np.complex128)).astype(np.float32)
    return x, P

# Uses voltage_power(), views() and fields() defined above:
# x13, P13 = reconstruct_d19(13)
# result13 = views(P13.astype(float), x13.astype(np.complex128))
# print(result13["BRIDE"])
#
# Expected: score approximately 0.42468361501242713,
#           groups 7 and 15.
#
# Additional-time excerpt at the same RF:
# x13_extra, P13_extra = reconstruct_d19(13, first_block=2)

N = 1048576
TB = 3.41333333333333e-7
TF = N * TB
F0 = 1668457031.25  # Hz

center_index = 63733
rf_center_hz = F0 - center_index / TF
