//  login.js
// function togglePassword() {
//   const input = document.getElementById("loginpassword"); // ✅ Corrected ID
//   const icon = document.getElementById("eyeIcon");

//   if (input.type === "password") {
//     input.type = "text";
//     icon.classList.replace("bi-eye", "bi-eye-slash");
//   } else {
//     input.type = "password";
//     icon.classList.replace("bi-eye-slash", "bi-eye");
//   }
// }
 
document.addEventListener("DOMContentLoaded", function () {
  const togglePassword = () => {
    const input = document.getElementById("loginpassword");
    const icon = document.getElementById("eyeIcon");

    if (input.type === "password") {
      input.type = "text";
      icon.classList.replace("bi-eye", "bi-eye-slash");
    } else {
      input.type = "password";
      icon.classList.replace("bi-eye-slash", "bi-eye");
    }
  };

  // Assign the function dynamically to the span
  const span = document.querySelector(".input-group-text");
  span.addEventListener("click", togglePassword);
});


//  register.js
function togglePassword(inputId, iconId) {
    const input = document.getElementById(inputId);
    const icon = document.getElementById(iconId);
  
    if (input.type === "password") {
      input.type = "text";
      icon.classList.replace("bi-eye", "bi-eye-slash");
    } else {
      input.type = "password";
      icon.classList.replace("bi-eye-slash", "bi-eye");
    }
  }
 

//  message.js
  // Automatically hide messages after 3 seconds
  setTimeout(function() {
    const messages = document.getElementById('messages');
    if (messages) {
      messages.style.display = 'none';
    }
  }, 5000);


//  vehicle.js
    // function searchVehicles() {
    //     let input = document.getElementById('searchInput').value.toLowerCase();
    //     let cards = document.querySelectorAll('.vehicle-card');

    //     cards.forEach(card => {
    //         let name = card.querySelector('.vehicle-name').textContent.toLowerCase();
    //         if (name.includes(input)) {
    //             card.style.display = 'block';
    //         } else {
    //             card.style.display = 'none';
    //         }
    //     });
    // }




 




    

  

//  bill.html
//   function calculate() {
//     var rent = parseInt(document.getElementById("vehRent").value);
//     var days = parseInt(document.getElementById("dayss").value);
//     var total = rent * days;

//     // Total Rent
//     document.querySelector("#rentsec span").textContent = total;

//     // Customer Name
//     var name = document.getElementById("billname").value;
//     document.querySelector("#n1 span").textContent = name;

//     // Pickup Location
//     var loc = document.getElementById("location").value;
//     document.querySelector("#l1 span").textContent = loc;

//     // Number of Days
//     document.querySelector("#d2 span").textContent = days;

//     // Pickup Date
//     var date = document.getElementById("date").value;
//     document.querySelector("#d1 span").textContent = date;

//     // Vehicle Name and Color (filled via template)
// // Vehicle Name
// document.querySelector("#crs1 span").textContent = document.querySelector("input[value='{{ vehicle.Vehicle_name }}']").value;

 

//     // Final Total
//     document.querySelector("#total span").textContent = total;
//   }

//   // Print button event
//   document.getElementById("btnPrint").onclick = function () {
//     printElement(document.getElementById("printThis"));
//   };

//   function printElement(elem) {
//     var domClone = elem.cloneNode(true);
//     var printSection = document.getElementById("printSection");

//     if (!printSection) {
//       printSection = document.createElement("div");
//       printSection.id = "printSection";
//       document.body.appendChild(printSection);
//     }

//     printSection.innerHTML = "";
//     printSection.appendChild(domClone);
//     window.print();
//   }
 
 
function calculate() {
  var rent = parseInt(document.getElementById("vehRent").value);
  var days = parseInt(document.getElementById("dayss").value);
  var total = rent * days;

  // Total Rent
  document.querySelector("#rentsec span").textContent = total;

  // Customer Name
  var name = document.getElementById("billname").value;
  document.querySelector("#n1 span").textContent = name;

  // Pickup Location
  var loc = document.getElementById("location").value;
  document.querySelector("#l1 span").textContent = loc;

  // Number of Days
  document.querySelector("#d2 span").textContent = days;

  const today = new Date();
  const options = { day: 'numeric', month: 'long', year: 'numeric' };
  document.getElementById("bookingDate").textContent = today.toLocaleDateString('en-GB', options);

  // Pickup Date
  var date = document.getElementById("date").value;
  document.querySelector("#d1 span").textContent = date;

  // Vehicle Name (filled via template)
  var vehicleName = document.getElementById("vehicleName").value;
  document.querySelector("#crs1 span").textContent = vehicleName;

  // Final Total
  document.querySelector("#total span").textContent = total;
}

// Bootstrap modal event listener to trigger calculation
var myModal = new bootstrap.Modal(document.getElementById('exampleModalLong'));
document.getElementById('exampleModalLong').addEventListener('shown.bs.modal', function () {
  calculate();  // Call calculate when the modal is shown
});

// Print button event
document.getElementById("btnPrint").onclick = function () {
  printElement(document.getElementById("printThis"));
};

function printElement(elem) {
  var domClone = elem.cloneNode(true);
  var printSection = document.getElementById("printSection");

  if (!printSection) {
    printSection = document.createElement("div");
    printSection.id = "printSection";
    document.body.appendChild(printSection);
  }

  printSection.innerHTML = "";
  printSection.appendChild(domClone);
  window.print();
}
 

 



