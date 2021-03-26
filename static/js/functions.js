
function submit () {
  let value = parseInt(document.getElementById('number').value, 10);
  value = isNaN(value) ? 0 : value;
  location.href = value;
  document.getElementById('number').value = value;
}
