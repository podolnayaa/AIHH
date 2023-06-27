// Update the relevant fields with the new data.
const setDOMInfo = info => {

	document.getElementById('result').innerHTML = info.res;
    document.getElementById('namee').innerHTML = "Обязанности объявления "+info.name+ ":"

    
};

window.addEventListener('DOMContentLoaded', () => {
	setTimeout( () => chrome.tabs.query( 
		{ active: true, currentWindow: true },
		tabs => { chrome.tabs.sendMessage(tabs[0].id, {from: 'index', subject: 'DOMInfo'}, setDOMInfo); }
		), 500);
});
