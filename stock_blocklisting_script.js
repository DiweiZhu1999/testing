// last update: Sept 6, 2023 by Diwei Zhu

// change this to include all URLs you want to submit to klue
urls = ['streetinsider.com',
 'biztoc.com',
 'benzinga.com',
 'msn.com',
 'markets.businessinsider.com',
 'morningstar.com',
 'investorsobserver.com',
 'fool.co.uk',
 'english.mubasher.info',
 'argaam.com',
 'tradingview.com',
 'blockchainmagazine.net',
 'theenterpriseleader.com',
 'stockpick.market',
 'steppingonacorns.typepad.com',
 'fool.com',
 'parktelegraph.com',
 'investorideas.com',
 'zacks.com',
 'shareandstocks.com',
 'seekingalpha.com',
 'finance.yahoo.com',
 'stockhouse.com',
 'beststocks.com',
 'capis.com',
 'insidermonkey.com',
 'marketingsentinel.com',
 'stocksregister.com',
 'cmcmarkets.com',
 'theconservativeinvestordaily.com',
 'newsheater.com',
 'moneycontrol.com',
 'sharecast.com',
 'stockmarketnerd',
 'capitalmarket.com',
 'chartsignals.blogspot.com',
 'investingnews.com',
 'zeebiz.com',
 'investegate.co.uk',
 'via.news',
 'marketnewsvideo.com',
 'cantechletter.com',
 'poundsterlinglive.com',
 'investchronicle.com',
 'schaeffersresearch.com',
 'tipranks.com',
 'livemint.com',
 'fool.com.au',
 'livewiremarkets.com',
 'kitco.com',
 'dwinnex.com',
 'vnexplorer.net',
 'invezz.com',
 'mediacoverage.com',
 'dailytradealert.com',
 'trefis.com',
 'shareprophets.com',
 'rttnews.com',
 'gettotext.com',
 'bizjournals.com',
 'inkl.com',
 'reedleyexponent.com',
 'scenefordummies.com',
 'cryptocompass.com',
 'plus500.com',
 'law360.com',
 'indiancrunch.in',
 'navajopost.org',
 'fool.ca',
 'transcriptdaily.com',
 'ukdaily.news',
 'bovnews.com'];

// DON'T CHANGE ANYTHING BEYOND THIS POINT!!!
// If you get an error, copy it and let us know.

// Make the ajax function available again
var jq = document.createElement('script');
jq.src = "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.4/jquery.min.js";
document.getElementsByTagName('head')[0].appendChild(jq);

// iterate and execute API call
for (let domain of urls) {
  await $.ajax({
    type: 'POST',
    url: '/api/source_preference/blocklist.json',
    dataType: 'json',
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify({ domain }),
    headers: {
      'X-CSRF-Token': document.querySelector('meta[name="csrf-token"]').content
    },
    success: ret => {
      console.log(`url '${domain}' added`);
    },
    error: (xhr, type) => {
      console.error('error adding "%s": %o, type: %o', domain, xhr, type);
    }
  });
}