/* fleet counts — one source of truth.
   Usage: <span data-count="deposits.total">…</span>
   Any element with data-count is filled from https://www.alexanarch.org/api/counts.json
   Dotted paths resolve into the JSON. Falls back silently to whatever text is already there,
   so a fetch failure degrades to the last known value rather than to an empty span. */
(function(){
  var SRC='https://www.alexanarch.org/api/counts.json';
  function dig(o,p){return p.split('.').reduce(function(a,k){return a&&a[k];},o);}
  function fmt(v){return typeof v==='number'?v.toLocaleString('en-US'):v;}
  function apply(d){
    document.querySelectorAll('[data-count]').forEach(function(el){
      var v=dig(d,el.getAttribute('data-count'));
      if(v!==undefined&&v!==null) el.textContent=fmt(v);
    });
    document.dispatchEvent(new CustomEvent('fleetcounts',{detail:d}));
  }
  try{
    var c=sessionStorage.getItem('fleetcounts');
    if(c) apply(JSON.parse(c));
  }catch(e){}
  fetch(SRC,{cache:'no-cache'}).then(function(r){return r.json()}).then(function(d){
    apply(d);
    try{sessionStorage.setItem('fleetcounts',JSON.stringify(d));}catch(e){}
  }).catch(function(){});
})();
