'use strict';
/* global XMLHttpRequest */
const deleteButtons = document.querySelectorAll('.delete');
const measurements = document.querySelector('#measurements');

function deleteThisMeasurementOnServer (e) {
  const id = e.target.attributes['data-id'].value;
  const requestURL = `${document.URL}/${id}`;
  const request = new XMLHttpRequest();
  request.addEventListener('load', function () {
    deleteThisMeasurementOnPage(id);
  });
  request.open('DELETE', requestURL, true);
  request.send();
}

function deleteThisMeasurementOnPage (id) {
  const selector = `#measurement-${id}`;
  const theMeasurement = document.querySelector(selector);
  console.log('selector =', selector, theMeasurement);
  if (theMeasurement) {
    measurements.removeChild(theMeasurement);
  } else {
    console.log('Trying to delete the deleted');
  }
}

if (deleteButtons) {
  for (const myButton of deleteButtons) {
    myButton.addEventListener('click', deleteThisMeasurementOnServer);
  }
}
