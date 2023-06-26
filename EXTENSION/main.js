'use strict';
window.setTimeout(function() {
    const descriptionBlockClass = '.g-user-content';
    const descriptionBlock = document.querySelectorAll(descriptionBlockClass);
    if (descriptionBlock != null) {
        //расширение отработает только если на странице обнаружиться блок с описанием объявления
        const descriptionText = document.querySelector(descriptionBlockClass).textContent;
        console.log(descriptionText);

        //тут блок с запросом и получением ответа от сервера
        function postData(url = "", data = {}) {

            fetch(url, {
                method: "POST",

                headers: {
                    "Content-Type": "application/json",

                },

                body: JSON.stringify(data), // body data type must match "Content-Type" header
            }).then(function(response) {
                console.log(response.json);

                if (response.ok) {
                    response.json()
                        .then(function(response) {
                            const myRES = response["response"];
                            // Inform the background page that
                            // this tab should have a page-action.
                            chrome.runtime.sendMessage({
                                from: 'content',
                                subject: 'showPageAction',
                            });

                            // Listen for messages from the popup.
                            chrome.runtime.onMessage.addListener((msg, sender, response) => {
                                // First, validate the message's structure.
                                if ((msg.from === 'index') && (msg.subject === 'DOMInfo')) {
                                    // Collect the necessary data.
                                    // (For your specific requirements `document.querySelectorAll(...)`
                                    //  should be equivalent to jquery's `$(...)`.)
                                    var domInfo = {
                                        res: myRES
                                    };

                                    // Directly respond to the sender (index),
                                    // through the specified callback.
                                    response(domInfo);
                                }
                            });

                            console.log(response);
                        });
                } else {
                    throw Error('Something went wrong');
                }
            })
                .catch(function(error) {
                    console.log(error);
                });

        }
        //сам запрос
        const ddata = {
            "descriptionText": descriptionText
        };
        //для отправки на свой сервер для тестировки, в конце работы нужно закомментить или удалить
        //postData("http://127.0.0.1:5000/predict", ddata);

    }
}, 1000);