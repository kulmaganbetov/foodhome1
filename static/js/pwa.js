function generate_pwa(logo, slug){
	var logo_src = "https://bad-catfish-10.loca.lt" + logo
      var myDynamicManifest = {
        "name": slug,
        "short_name": slug,
        "start_url": "https://gosite.kz/" + slug,
        "display": "standalone",
        "background_color": "#FFF",
        "theme_color": "#493174",
        "description": slug,
        "dir": "ltr",
        "lang": "en-US",
        "orientation": "any",
        "icons": [
            {
              "src": logo_src,
              "sizes": "48x48"
            },
            {
              "src": logo_src,
              "sizes": "96x96 128x128 256x256"
            },
            {
              "src": logo_src,
              "sizes": "257x257"
            }
        ]
      }
      const stringManifest = JSON.stringify(myDynamicManifest);
      const blob = new Blob([stringManifest], {type: 'application/json'});
      const manifestURL = URL.createObjectURL(blob);
      document.querySelector('#manifest').setAttribute('href', manifestURL);
}