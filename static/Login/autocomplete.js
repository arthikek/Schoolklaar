
function initMapsAPI() {
    initAutocomplete();
  }
  

function initAutocomplete() {
    const input1 = document.getElementById('formGroupExampleInput2');
    const input2 = document.getElementById('formGroupExampleInput3');
  
    const options = {
      componentRestrictions: { country: 'nl' },
      fields: ['address_components', 'geometry', 'icon', 'name'],
    };
  
    const autocomplete1 = new google.maps.places.Autocomplete(input1, options);
    const autocomplete2 = new google.maps.places.Autocomplete(input2, options);
  
    // Add event listeners to check for errors
    google.maps.event.addListener(autocomplete1, 'place_changed', function () {
      if (autocomplete1.getPlace().error_message) {
        console.error('Error: ' + autocomplete1.getPlace().error_message);
      }
    });
  
    google.maps.event.addListener(autocomplete2, 'place_changed', function () {
      if (autocomplete2.getPlace().error_message) {
        console.error('Error: ' + autocomplete2.getPlace().error_message);
      }
    });
  }
  
  document.addEventListener('DOMContentLoaded', () => {
    initMapsAPI();
  });
  