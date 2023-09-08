$.noConflict();

jQuery(document).ready(function($) {

	"use strict";

	[].slice.call( document.querySelectorAll( 'select.cs-select' ) ).forEach( function(el) {
		new SelectFx(el);
	});

	jQuery('.selectpicker').selectpicker;


	

	$('.search-trigger').on('click', function(event) {
		event.preventDefault();
		event.stopPropagation();
		$('.search-trigger').parent('.header-left').addClass('open');
	});

	$('.search-close').on('click', function(event) {
		event.preventDefault();
		event.stopPropagation();
		$('.search-trigger').parent('.header-left').removeClass('open');
	});

	$('.equal-height').matchHeight({
		property: 'max-height'
	});


	$('.count').each(function () {
		$(this).prop('Counter',0).animate({
			Counter: $(this).text()
		}, {
			duration: 3000,
			easing: 'swing',
			step: function (now) {
				$(this).text(Math.ceil(now));
			}
		});
	});


	// Menu Trigger
	$('#menuToggle').on('click', function(event) {
		var windowWidth = $(window).width();   		 
		if (windowWidth<1010) { 
			$('body').removeClass('open'); 
			if (windowWidth<760){ 
				$('#left-panel').slideToggle(); 
			} else {
				$('#left-panel').toggleClass('open-menu');  
			} 
		} else {
			$('body').toggleClass('open');
			$('#left-panel').removeClass('open-menu');  
		} 
			 
	}); 

	 
	$(".menu-item-has-children.dropdown").each(function() {
		$(this).on('click', function() {
			var $temp_text = $(this).children('.dropdown-toggle').html();
			$(this).children('.sub-menu').prepend('<li class="subtitle">' + $temp_text + '</li>'); 
		});
	});

	$(window).on("load resize", function(event) { 
		var windowWidth = $(window).width();  		 
		if (windowWidth<1010) {
			$('body').addClass('small-device'); 
		} else {
			$('body').removeClass('small-device');  
		} 
		
	});
  
 
});

function validatePage1() {
    var first_name = document.getElementById('first-name').value.trim();
    var last_name = document.getElementById('last-name').value.trim();
    var email = document.getElementById('email').value.trim();
    var phone = document.getElementById('phone').value.trim();

    if (first_name === '' || last_name === '' || email === '' || phone === '') {
        alert('Please fill in all fields on this page.');
        return false;
    }

    return true;
}

function validatePage2() {
    var address1 = document.getElementById('address-line-1').value.trim();
    var city = document.getElementById('city').value.trim();
    var state = document.getElementById('state').value.trim();
    var zip_code = document.getElementById('zip').value.trim();

    if (address1 === '' || city === '' || state === '' || zip_code === '') {
        alert('Please fill in all fields on this page.');
        return false;
    }

    return true;
}

function validatePage3() {
    var username = document.getElementById('username').value.trim();
    var password = document.getElementById('password').value.trim();
    var confirm_password = document.getElementById('confirm_password').value.trim();

    if (username === '' || password === '' || confirm_password === '') {
        alert('Please fill in all fields on this page.');
        return false;
    }

    if (password !== confirm_password) {
        alert('Passwords do not match.');
        return false;
    }

    return true;
}

function validatePage4() {
    return true;
}

function submitForm() {
    // Final form submission logic
    alert("Form submitted successfully!");
}

function nextPage(currentPage) {
    let nextTab = currentPage + 1;
    let currentTab = document.getElementById("selection_tab" + currentPage);
    let nextTabContent = document.getElementById("selection_tab" + nextTab);

    if (currentPage < 4 && validatePage(currentPage)) {
        currentTab.classList.remove("active");
        nextTabContent.style.display = "block";
        document.getElementById("selection_tab" + nextTab).classList.add("active");
        document.getElementById("selection_tab" + currentPage).style.display = "none";
    }
}

function previousPage(currentPage) {
    let prevTab = currentPage - 1;
    let currentTab = document.getElementById("selection_tab" + currentPage);
    let prevTabContent = document.getElementById("selection_tab" + prevTab);

    if (currentPage > 1 && validatePage(currentPage - 1)) {
        currentTab.classList.remove("active");
        prevTabContent.style.display = "block";
        document.getElementById("selection_tab" + prevTab).classList.add("active");
        document.getElementById("selection_tab" + currentPage).style.display = "none";
    }
}

function validatePage(currentPage) {
    switch (currentPage) {
        case 1:
            return validatePage1();
        case 2:
            return validatePage2();
        case 3:
            return validatePage3();
        case 4:
            return validatePage4();
        default:
            return true;
    }
}

function checkPassword() {
  var password = document.getElementById("password");
  var confirm_password = document.getElementById("confirm_password");
  var password_warning = document.getElementById("password_warning");

  if (password.value != confirm_password.value) {
    password_warning.style.display = "inline";
  } else {
    password_warning.style.display = "none";
  }
}

// Function to check if an element is in the viewport
function isElementInViewport(el) {
    var rect = el.getBoundingClientRect();
    return (
      rect.top >= 0 &&
      rect.left >= 0 &&
      rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
      rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );


// Function to load more items when user scrolls
function lazyLoad() {
    var mediaItems = document.getElementsByClassName("media-item");

    for (var i = 0; i < mediaItems.length; i++) {
      if (isElementInViewport(mediaItems[i])) {
        mediaItems[i].classList.add("loaded");
      }
    }
}

// Attach lazyLoad function to scroll event
window.addEventListener("scroll", lazyLoad);

// Load initial items
lazyLoad();