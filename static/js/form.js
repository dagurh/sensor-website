'use strict';

const form = document.querySelector('#greetings-form');
const temperature = document.querySelector('#temperature');
const humidity = document.querySelector('#humidity');
const pressure = document.querySelector('#pressure');
const temperatureFeedback = document.querySelector('#temperature-feedback');
const humidityFeedback = document.querySelector('#humidity-feedback');
const pressureFeedback = document.querySelector('#pressure-feedback');

form.addEventListener('submit', (e) => {
  if (temperature.value === '') {
    e.preventDefault();
    temperatureFeedback.textContent = 'Please add a temperature';
  } else {
    temperatureFeedback.textContent = '';
  }
  if (humidity.value === '') {
    e.preventDefault();
    humidityFeedback.textContent = 'Please add a humidity';
  } else {
    humidityFeedback.textContent = '';
  }
  if (pressure.value === '') {
    e.preventDefault();
    pressureFeedback.textContent = 'Please add a pressure';
  } else {
    pressureFeedback.textContent = '';
  }
});
