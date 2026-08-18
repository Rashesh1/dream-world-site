/* Dream World — shell injection + rendering. Vanilla, no deps. */
(function(){
  var C = window.DW_CONFIG, P = window.DW_PRODUCTS || [];
  var HOME = !/collection\.html|product\.html/.test(location.pathname);
  var rupee = function(n){ return "₹" + n.toLocaleString("en-IN"); };
  var priceLabel = function(p){ return p==null ? "Enquire for price" : rupee(p); };
  var waLink = function(text){ return "https://wa.me/" + C.whatsapp + "?text=" + encodeURIComponent(text); };
  var anchor = function(id){ return (HOME ? "" : "index.html") + "#" + id; };
  var catHref = function(slug){ return "collection.html?cat=" + slug; };
  var productHref = function(sku){ return "product.html?sku=" + encodeURIComponent(sku); };
  var WA_ICON = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38a9.9 9.9 0 0 0 4.79 1.22h.01c5.46 0 9.91-4.45 9.91-9.91S17.5 2 12.04 2Zm5.8 14.03c-.24.68-1.4 1.3-1.94 1.38-.5.07-1.13.1-1.82-.11-.42-.13-.96-.31-1.65-.61-2.9-1.25-4.8-4.17-4.94-4.36-.15-.19-1.19-1.58-1.19-3.01 0-1.43.75-2.13 1.02-2.42.27-.29.58-.36.78-.36.19 0 .39 0 .56.01.18.01.42-.07.66.5.24.58.82 2.01.89 2.16.07.14.12.31.02.5-.09.19-.14.31-.28.48-.14.17-.29.37-.42.5-.14.14-.28.29-.12.57.16.29.71 1.17 1.53 1.9 1.05.94 1.94 1.23 2.22 1.37.28.14.44.12.6-.07.16-.19.69-.81.87-1.09.18-.28.36-.23.6-.14.24.09 1.55.73 1.82.86.27.14.44.21.5.32.07.11.07.63-.17 1.31Z"/></svg>';
  var ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
  function el(html){ var d=document.createElement("div"); d.innerHTML=html.trim(); return d.firstChild; }

  var NAV = [["Beds",catHref("beds")],["Sofas",catHref("sofas")],["Loungers",catHref("loungers")],
             ["Tables",catHref("tables")],["Reviews",anchor("reviews")],["Visit us",anchor("visit")]];
  var DRAWER_NAV = C.categories.map(function(c){return [c.label, catHref(c.slug)];})
    .concat([["Reviews",anchor("reviews")],["Visit us",anchor("visit")]]);

  /* ---------- header ---------- */
  function header(){
    var links = NAV.map(function(x){return '<a href="'+x[1]+'">'+x[0]+'</a>';}).join("");
    var h = el(
      '<header class="hdr"><div class="hdr-in">'
      + '<a class="brand" href="index.html" aria-label="Dream World home">'
      + '<img class="brand-logo" src="assets/img/brand/logo.png" alt="Dream World" '
      + 'onerror="this.style.display=\'none\';this.nextElementSibling.style.display=\'inline-flex\'">'
      + '<span class="brand-mark" style="display:none"><b>DREAM WORLD</b></span></a>'
      + '<nav class="nav">'+links+'</nav>'
      + '<div class="hdr-cta">'
      + '<button class="search-btn" aria-label="Search products" aria-expanded="false">'
      + '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.35-4.35"/></svg></button>'
      + '<a class="btn btn-ghost" href="tel:'+C.phone+'"><span>Call</span></a>'
      + '<button class="menu-btn" aria-label="Open menu" aria-expanded="false">'
      + '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button>'
      + '</div></div>'
      + '<div class="search-panel" id="search-panel" hidden>'
      + '<div class="wrap search-panel-in">'
      + '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="search-ico"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.35-4.35"/></svg>'
      + '<input type="text" id="search-input" placeholder="Search beds, sofas, mattress, and more..." autocomplete="off">'
      + '<button class="search-close" aria-label="Close search">×</button>'
      + '</div>'
      + '<div class="search-results wrap" id="search-results"></div>'
      + '</div></header>');
    document.getElementById("header").replaceWith(h);
    if(document.querySelector(".hero")) h.classList.add("over-hero");
    var onScroll=function(){ h.classList.toggle("scrolled", window.scrollY>8); };
    onScroll(); window.addEventListener("scroll", onScroll, {passive:true});
    drawer(h);
    search(h);
  }

  /* ---------- search + autocomplete ---------- */
  function search(h){
    var panel=document.getElementById("search-panel");
    var btn=h.querySelector(".search-btn");
    var input=document.getElementById("search-input");
    var results=document.getElementById("search-results");
    var closeBtn=panel.querySelector(".search-close");
    function open(){
      panel.hidden=false; btn.setAttribute("aria-expanded","true");
      setTimeout(function(){ input.focus(); },10);
    }
    function close(){
      panel.hidden=true; btn.setAttribute("aria-expanded","false");
      input.value=""; results.innerHTML="";
    }
    btn.addEventListener("click",function(){ panel.hidden ? open() : close(); });
    closeBtn.addEventListener("click",close);
    document.addEventListener("keydown",function(e){ if(e.key==="Escape" && !panel.hidden) close(); });

    function render(q){
      q=q.trim().toLowerCase();
      if(!q){ results.innerHTML=""; return; }
      var catMatch = C.categories.filter(function(c){
        return c.label.toLowerCase().indexOf(q)>-1 || c.slug.indexOf(q)>-1;
      });
      var prodMatch = P.filter(function(p){
        return p.name.toLowerCase().indexOf(q)>-1 || p.categoryLabel.toLowerCase().indexOf(q)>-1;
      }).slice(0,6);
      if(!catMatch.length && !prodMatch.length){
        results.innerHTML='<p class="search-empty">No matches. Try "bed", "sofa", "mattress"…</p>';
        return;
      }
      var html="";
      catMatch.slice(0,2).forEach(function(c){
        var count=P.filter(function(p){return p.category===c.slug;}).length;
        html += '<a class="search-row search-row-cat" href="'+catHref(c.slug)+'">'
          + '<span class="search-row-icon">'+ARROW+'</span>'
          + '<span><b>'+c.label+'</b><small>View all '+count+' designs →</small></span></a>';
      });
      prodMatch.forEach(function(p){
        html += '<a class="search-row" href="'+productHref(p.sku)+'">'
          + '<img src="'+p.img+'" alt="" loading="lazy">'
          + '<span><b>'+p.name+'</b><small>'+p.categoryLabel+' · '+priceLabel(p.price)+'</small></span></a>';
      });
      results.innerHTML=html;
    }
    input.addEventListener("input",function(){ render(input.value); });
  }

  /* ---------- mobile drawer ---------- */
  function drawer(h){
    var d = el(
      '<div class="drawer" id="drawer" hidden><div class="drawer-panel" role="dialog" aria-label="Menu">'
      + '<button class="drawer-close" aria-label="Close menu">×</button>'
      + '<nav class="drawer-nav">' + DRAWER_NAV.map(function(x){return '<a href="'+x[1]+'">'+x[0]+'</a>';}).join("") + '</nav>'
      + '<div class="drawer-cta">'
      + '<a class="btn btn-wa" href="'+waLink("Hi Dream World, I\'d like to enquire about your furniture.")+'" target="_blank" rel="noopener">'+WA_ICON+'<span>WhatsApp</span></a>'
      + '<a class="btn btn-ghost" href="tel:'+C.phone+'"><span>Call '+C.phone+'</span></a>'
      + '</div></div></div>');
    document.body.appendChild(d);
    var open=function(v){ d.hidden=!v; document.body.style.overflow=v?"hidden":""; h.querySelector(".menu-btn").setAttribute("aria-expanded",v); };
    h.querySelector(".menu-btn").addEventListener("click",function(){open(true);});
    d.querySelector(".drawer-close").addEventListener("click",function(){open(false);});
    d.addEventListener("click",function(e){ if(e.target===d||e.target.closest("a")) open(false); });
  }

  /* ---------- footer ---------- */
  function footer(){
    var f = el(
      '<footer class="ft"><div class="wrap">'
      + '<div class="ft-top">'
      + '<div><h4>Dream World</h4><p class="ft-addr">'+C.address+'</p>'
      + '<p class="ft-addr" style="margin-top:.8rem">Made-to-order beds, sofas, loungers and tables. Delivered across North India.</p></div>'
      + '<div><h4>Explore</h4><a href="'+catHref("beds")+'">Beds</a><a href="'+catHref("sofas")+'">Sofas</a><a href="'+catHref("loungers")+'">Loungers</a><a href="'+catHref("tables")+'">Center tables</a></div>'
      + '<div><h4>Connect</h4>'
      + '<a href="'+waLink("Hi Dream World!")+'" target="_blank" rel="noopener">WhatsApp</a>'
      + '<a href="tel:'+C.phone+'">'+C.phone+'</a>'
      + '<a href="'+C.instagram+'" target="_blank" rel="noopener">Instagram</a>'
      + '<a href="'+anchor("visit")+'">Visit us</a></div>'
      + '</div>'
      + '<div class="ft-bot"><span>© '+new Date().getFullYear()+' Dream World, Dehradun. All rights reserved.</span>'
      + '<span>Made to order · Prices shown are indicative — confirm on WhatsApp.</span></div>'
      + '</div></footer>');
    document.getElementById("footer").replaceWith(f);
  }

  /* ---------- floating WA ---------- */
  function floatWA(){
    document.body.appendChild(el(
      '<a class="wa-float" href="'+waLink("Hi Dream World, I saw your website and want to enquire.")+'" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">'
      +WA_ICON+'<span class="lbl">Chat with us</span></a>'));
  }

  /* ---------- product card — whole card leads to its detail page ---------- */
  function card(p, showSpec){
    var href = productHref(p.sku);
    return '<article class="card reveal">'
      + '<a class="card-media" href="'+href+'" aria-label="View '+p.name+'"><img src="'+p.img+'" alt="'+p.name+'" loading="lazy"></a>'
      + '<div class="card-body"><span class="cat">'+p.categoryLabel+'</span>'
      + '<a href="'+href+'" class="card-title-link"><h3>'+p.name+'</h3></a>'
      + (showSpec&&p.specs?'<p class="cspec">'+p.specs+'</p>':'')
      + '<div class="price">'+(p.price==null
          ? '<b class="price-enquire">Enquire for price</b>'
          : '<b>'+rupee(p.price)+'</b><small>onwards</small>')+'</div>'
      + '<a class="enquire" href="'+href+'"><span>View design</span>'+ARROW+'</a>'
      + '</div></article>';
  }

  /* ---------- category cards (home) ---------- */
  var THUMB={ beds:"assets/img/products/bed-04.jpg", sofas:"assets/img/products/sofa-03.jpg",
              loungers:"assets/img/products/lounger-07.jpg", tables:"assets/img/products/table-06.jpg",
              "sofa-cum-bed":"assets/img/categories/sofa-cum-bed.jpg", mattress:"assets/img/categories/mattress.jpg",
              "pillow-cushion":"assets/img/products/pillow-02-comfort-cool.jpg",
              "dining-table":"assets/img/categories/dining-table.jpg", "tv-cabinet":"assets/img/categories/tv-cabinet.jpg",
              interior:"assets/img/categories/interior.jpg" };
  var THUMB_SOON={ interior:"assets/img/categories/interior.jpg" };
  function categories(){
    var g=document.getElementById("cat-grid"); if(!g) return;
    var live = C.categories.map(function(c){
      var count=P.filter(function(p){return p.category===c.slug;}).length;
      return '<a class="cat-card reveal" href="'+catHref(c.slug)+'">'
        + '<img src="'+(THUMB[c.slug]||"")+'" alt="'+c.label+'" loading="lazy">'
        + '<div class="cat-body"><h3>'+c.label+'</h3><span class="tag">'+c.tag+' · '+count+' designs</span>'
        + '<span class="arrow">View collection →</span></div></a>';
    }).join("");
    var soon = (C.categoriesComingSoon||[]).map(function(c){
      var img=THUMB_SOON[c.slug];
      return '<div class="cat-card cat-card-soon reveal">'
        + (img?'<img src="'+img+'" alt="'+c.label+'" loading="lazy">':'')
        + '<div class="cat-body"><span class="soon-badge">Coming soon</span><h3>'+c.label+'</h3>'
        + '<span class="tag">'+c.tag+'</span>'
        + '<a class="arrow" href="'+waLink("Hi Dream World, I\'m interested in "+c.label+" — do you have designs to show me?")+'" target="_blank" rel="noopener">Ask on WhatsApp →</a>'
        + '</div></div>';
    }).join("");
    g.innerHTML = live + soon;
  }

  /* ---------- home featured (2 per category) ---------- */
  function featured(){
    var g=document.getElementById("featured-grid"); if(!g) return;
    var picks=[];
    C.categories.forEach(function(c){ picks=picks.concat(P.filter(function(p){return p.category===c.slug;}).slice(0,2)); });
    g.innerHTML=picks.map(function(p){return card(p,false);}).join("");
    observe();
  }

  /* ---------- collection page (filterable) ---------- */
  function collection(){
    var grid=document.getElementById("prod-grid"), chips=document.getElementById("chips");
    if(!grid||!chips) return;
    var cats=[{slug:"all",label:"All"}].concat(C.categories.map(function(c){return {slug:c.slug,label:c.label};}));
    var initial=(new URLSearchParams(location.search).get("cat"))||"all";
    if(!cats.some(function(c){return c.slug===initial;})) initial="all";
    chips.innerHTML=cats.map(function(c){return '<button class="chip'+(c.slug===initial?" active":"")+'" data-f="'+c.slug+'">'+c.label+'</button>';}).join("");
    function setTitle(f){
      var t=document.getElementById("collection-title");
      if(t) t.textContent = f==="all" ? "All furniture" : (cats.filter(function(c){return c.slug===f;})[0].label);
      var desc=document.getElementById("cat-desc"), dtext=document.getElementById("cat-desc-text");
      var text = (C.categoryDescriptions||{})[f];
      if(desc && dtext){
        if(text){ dtext.textContent=text; desc.hidden=false; } else { desc.hidden=true; }
      }
    }
    function render(f){
      var list=f==="all"?P:P.filter(function(p){return p.category===f;});
      grid.innerHTML=list.map(function(p){return card(p,true);}).join("");
      setTitle(f); observe();
    }
    chips.addEventListener("click",function(e){
      var b=e.target.closest(".chip"); if(!b) return;
      chips.querySelectorAll(".chip").forEach(function(c){c.classList.remove("active");});
      b.classList.add("active"); render(b.dataset.f);
      history.replaceState(null,"",catHref(b.dataset.f));
    });
    render(initial);
  }

  /* ---------- instagram ---------- */
  function instagram(){
    var iv=document.getElementById("insta-visit"); if(iv) iv.href=C.instagram;
  }

  /* ---------- reviews (placeholder until live Google feed wired) ---------- */
  var REVIEWS = window.DW_REVIEWS || [
    {n:"Priya S.",t:"Got a king storage bed made to order. Finish is premium and delivery was on time. Very happy.",r:5},
    {n:"Aman R.",t:"Sofa quality is solid — real wood frame, thick foam. Better value than the big showrooms.",r:5},
    {n:"Neha K.",t:"They helped me pick the fabric on WhatsApp and shared updates till delivery. Smooth experience.",r:5},
  ];
  function reviews(){
    var g=document.getElementById("review-grid"); if(!g) return;
    g.innerHTML=REVIEWS.map(function(rv){
      return '<figure class="review reveal"><div class="rstars" aria-label="'+rv.r+' out of 5">'
        + "★★★★★".slice(0,rv.r)+'</div><blockquote>“'+rv.t+'”</blockquote>'
        + '<figcaption>'+rv.n+' · <span>Google</span></figcaption></figure>';
    }).join("");
    var link = C.googleReviews || C.googleMaps || ("https://www.google.com/maps/search/"+encodeURIComponent("Dream World "+C.address));
    var all=document.getElementById("all-reviews"); if(all) all.href=link;
    var rc=document.getElementById("review-count"); if(rc&&C.reviewCount) rc.textContent=C.reviewCount+" Google reviews";
  }

  /* ---------- owner ---------- */
  function owner(){
    var o=C.owner; if(!o) return;
    var img=document.getElementById("owner-img");
    if(img){ img.alt=o.name; img.src=o.img; }
    var fb=document.querySelector(".owner-fallback");
    if(fb) fb.textContent=o.name.split(" ").map(function(w){return w[0];}).join("").slice(0,2).toUpperCase();
    var n=document.getElementById("owner-name"); if(n) n.textContent=o.name;
    var r=document.getElementById("owner-role"); if(r) r.textContent=o.role;
  }

  /* ---------- visit ---------- */
  function visit(){
    var a=document.getElementById("visit-addr"); if(a) a.textContent=C.address;
    var p=document.getElementById("visit-phone"); if(p) p.textContent=C.phone;
    var vw=document.getElementById("visit-wa"); if(vw){ vw.href=waLink("Hi Dream World, I'd like to visit your workshop. Please share the exact location."); vw.target="_blank"; }
    var dir=document.getElementById("visit-dir");
    if(dir) dir.href = C.googleMaps || ("https://www.google.com/maps/dir/?api=1&destination="+encodeURIComponent(C.address));
  }

  /* ---------- hero / dist WA links ---------- */
  function links(){
    var hw=document.getElementById("hero-wa");
    if(hw){ hw.href=waLink("Hi Dream World, I'd like to see your furniture designs and prices."); hw.target="_blank"; }
    var dw=document.getElementById("dist-wa");
    if(dw){ dw.href=waLink("Hi Dream World, I'm a dealer interested in your distributor program."); dw.target="_blank"; }
    var iw=document.getElementById("inspire-wa");
    if(iw){ iw.href=waLink("Hi Dream World, I saw a design I love and want you to build it for me. Sharing the photo now."); iw.target="_blank"; }
  }

  /* ---------- per-category customization options ----------
     Only offered where the choice genuinely varies by category. */
  var CUSTOM_CONFIG = {
    "beds": [["size",["Single","Queen","King","Custom size"]],["material",["Leatherette","Fabric","Velvet","Wood tone"]],["colour",["Beige","Grey","Navy","Custom shade"]]],
    "sofas": [["size",["2-Seater","3-Seater","L-Shape","Custom size"]],["material",["Leatherette","Fabric","Velvet"]],["colour",["Beige","Grey","Navy","Custom shade"]]],
    "sofa-cum-bed": [["size",["Single","Double","Custom size"]],["material",["Fabric","Leatherette","Wood tone"]],["colour",["Beige","Grey","Navy","Custom shade"]]],
    "loungers": [["material",["Fabric","Velvet","Leatherette"]],["colour",["Beige","Grey","Navy","Custom shade"]]],
    "tables": [["material",["Sheesham","Acacia","Mango Wood","Custom"]]],
    "mattress": [["size",["Single","Double","Queen","King"]],["firmness",["Soft","Medium","Firm","Orthopedic"]]],
    "pillow-cushion": [],
  };

  /* ---------- product detail page ---------- */
  function productDetail(){
    var nameEl=document.getElementById("pdp-name"); if(!nameEl) return;
    var sku=new URLSearchParams(location.search).get("sku");
    var p=P.filter(function(x){return x.sku===sku;})[0] || P[0];
    if(!p) return;
    document.title=p.name+" — Dream World";
    document.getElementById("pdp-img").src=p.img;
    document.getElementById("pdp-img").alt=p.name;
    document.getElementById("pdp-cat").textContent=p.categoryLabel;
    nameEl.textContent=p.name;
    var priceEl=document.getElementById("pdp-price");
    priceEl.textContent=priceLabel(p.price);
    priceEl.parentElement.querySelector("small").style.display = p.price==null ? "none" : "";
    document.getElementById("pdp-specs-text").textContent=p.specs||"Details shared on request.";
    document.getElementById("sticky-price").textContent=priceLabel(p.price);
    document.getElementById("sticky-name").textContent=p.name;
    var back=document.getElementById("pdp-back-cat"); if(back) back.href=catHref(p.category);

    var prefs={};
    var waBtn=document.getElementById("pdp-wa");
    function buildMsg(){
      var priceTxt = p.price==null ? "price on request" : rupee(p.price)+" onwards";
      var lines=["Hi Dream World, I'm interested in the "+p.name+" ("+p.sku+", "+priceTxt+")."];
      var keys=Object.keys(prefs).filter(function(k){return prefs[k];});
      if(keys.length){
        var chosen=keys.map(function(k){return k.charAt(0).toUpperCase()+k.slice(1)+": "+prefs[k];});
        lines.push("My preference — "+chosen.join(", ")+".");
      }
      lines.push("Please confirm exact sizing, material and best price.");
      return lines.join(" ");
    }
    function updateWA(){ waBtn.href=waLink(buildMsg()); waBtn.target="_blank"; }
    updateWA();

    var customBlock=document.getElementById("pdp-custom");
    var customGroups=document.getElementById("pdp-custom-groups");
    var groups = CUSTOM_CONFIG[p.category] || [];
    if(groups.length && customBlock && customGroups){
      customBlock.hidden=false;
      customGroups.innerHTML = groups.map(function(g){
        var key=g[0], label=key.charAt(0).toUpperCase()+key.slice(1), opts=g[1];
        return '<div class="chip-group" data-group="'+key+'"><span class="chip-label">'+label+'</span>'
          + '<div class="chips">' + opts.map(function(o){return '<button class="chip" type="button">'+o+'</button>';}).join("") + '</div></div>';
      }).join("");
      customGroups.querySelectorAll(".chip-group").forEach(function(g){
        var key=g.dataset.group;
        g.addEventListener("click",function(e){
          var b=e.target.closest(".chip"); if(!b) return;
          var was=b.classList.contains("active");
          g.querySelectorAll(".chip").forEach(function(c){c.classList.remove("active");});
          if(was){ delete prefs[key]; } else { b.classList.add("active"); prefs[key]=b.textContent.trim(); }
          updateWA();
        });
      });
    }

    var relGrid=document.getElementById("related-grid");
    if(relGrid){
      var rel=P.filter(function(x){return x.category===p.category && x.sku!==p.sku;}).slice(0,4);
      relGrid.innerHTML=rel.map(function(x){return card(x,false);}).join("");
      observe();
    }
  }

  /* ---------- reveal observer ---------- */
  var io;
  function observe(){
    if(!("IntersectionObserver" in window)){ document.querySelectorAll(".reveal").forEach(function(n){n.classList.add("in");}); return; }
    if(!io) io=new IntersectionObserver(function(es){es.forEach(function(en){ if(en.isIntersecting){ en.target.classList.add("in"); io.unobserve(en.target);} });},{threshold:.1,rootMargin:"0px 0px -6% 0px"});
    document.querySelectorAll(".reveal:not(.in)").forEach(function(n){io.observe(n);});
  }

  header(); footer(); floatWA(); categories(); featured(); collection(); productDetail(); instagram(); owner(); reviews(); visit(); links(); observe();
})();
