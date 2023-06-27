chrome.runtime.onMessage.addListener((msg, sender) => {
    // First, validate the message's structure.
    if ((msg.from === 'content') && (msg.subject === 'showPageAction')) {
		 /*var views = chrome.extension.getViews({
			type: "popup"
		});
		for (var i = 0; i < views.length; i++) {
			views[i].document.getElementById('result').innerHTML = response["response"];
		}*/
      // Enable the page-action for the requesting tab.
      //chrome.pageAction.show(sender.tab.id);
	  //chrome.action.openPopup();
	  //chrome.action.setPopup({popup: ""});
	  //chrome.action.setPopup({popup: "index.html"});
    }
  });