'use strict';
/* global XMLHttpRequest */
const deleteButtons = document.querySelectorAll('.delete');
const greetings = document.querySelector('#greetings');

function deleteThisGreetingOnServer (e) {
  const id = e.target.attributes['data-id'].value;
  const requestURL = `${document.URL}/${id}`;
  const request = new XMLHttpRequest();
  request.addEventListener('load', function () {
    deleteThisGreetingOnPage(id);
  });
  request.open('DELETE', requestURL, true);
  request.send();
}

function deleteThisGreetingOnPage (id) {
  const selector = `#greeting-${id}`;
  const theGreeting = document.querySelector(selector);
  console.log('selector =', selector, theGreeting);
  if (theGreeting) {
    greetings.removeChild(theGreeting);
  } else {
    console.log('Trying to delete the deleted');
  }
}

if (deleteButtons) {
  for (const myButton of deleteButtons) {
    myButton.addEventListener('click', deleteThisGreetingOnServer);
  }
}
