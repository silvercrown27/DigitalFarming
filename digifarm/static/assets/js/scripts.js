$.noConflict();

jQuery(document).ready(function ($) {
    "use strict";

    [].slice.call(document.querySelectorAll('select.cs-select')).forEach(function (el) {
        new SelectFx(el);
    });

    jQuery('.selectpicker').selectpicker;

    $('.equal-height').matchHeight({
        property: 'max-height'
    });

    $('.count').each(function () {
        $(this).prop('Counter', 0).animate({
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
    $('#menuToggle').on('click', function (event) {
        var windowWidth = $(window).width();

        // Toggle the 'open' class on body
        $('body').toggleClass('open');

        // Toggle the 'hide-logo' class on menu toggle click
        $('.menu-toggle-wrapper').toggleClass('hide-logo');

        if (windowWidth < 1010) {
            if (windowWidth < 760) {
                $('#left-panel').slideToggle();
            } else {
                $('#left-panel').toggleClass('open-menu');
            }
        } else {
            $('#left-panel').removeClass('open-menu');
        }
    });

    $(".menu-item-has-children.dropdown").each(function () {
        $(this).on('click', function () {
            var $temp_text = $(this).children('.dropdown-toggle').html();
            $(this).children('.sub-menu').prepend('<li class="subtitle">' + $temp_text + '</li>');
        });
    });

    $(window).on("load resize", function (event) {
        var windowWidth = $(window).width();
        if (windowWidth < 1010) {
            $('body').addClass('small-device');
        } else {
            $('body').removeClass('small-device');
        }
    });
});


function validatePage1() {
    // Validation logic for page 1
    return true; // Return true if validation is successful, false otherwise
}

function validatePage2() {
    // Validation logic for page 2
    return true; // Return true if validation is successful, false otherwise
}

function validatePage3() {
    // Validation logic for page 3
    return true; // Return true if validation is successful, false otherwise
}

function validatePage4() {
    // Validation logic for page 4
    return true; // Return true if validation is successful, false otherwise
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
}

(function ($) {
    $(document).ready(function () {
        var openChatButton = $('#openChat');
        var chatBox = $('#chatBox');

        openChatButton.on('click', function () {
            if (chatBox.css('display') === 'none') {
                chatBox.css('display', 'block');
            } else {
                chatBox.css('display', 'none');
            }
        });
    });
})(jQuery);


(function ($) {
    var btnUpload = $("#upload_file");
    var btnOuter = $(".button_outer");
    var uploadedImageContainer = $("#uploaded_file_view");
    var errorMessageContainer = $(".error_msg");
    var successBox = $(".success_box");
    var processingBar = $(".processing_bar");
    var uploadLabel = $("#upload_label");

    btnUpload.on("change", function (e) {
        var ext = btnUpload.val().split('.').pop().toLowerCase();
        if ($.inArray(ext, ['gif', 'png', 'jpg', 'jpeg']) === -1) {
            errorMessageContainer.text("Not an Image...");
        } else {
            errorMessageContainer.text("");
            btnOuter.addClass("file_uploading");

            var errorOccurred = false;

            var formData = new FormData();
            formData.append('img_upload', e.target.files[0]);

            $.ajaxSetup({
                headers: {
                    "X-CSRFToken": csrfToken
                }
            });

            $.ajax({
                type: "POST",
                url: "/upload/",
                data: formData,
                processData: false,
                contentType: false,
                beforeSend: function () {
                    processingBar.css('display', 'block');
                },
                success: function (response) {
                    processingBar.css('display', 'none');
                    if (response.hasOwnProperty('image_path')) {
                        var imageUrl = response.image_url;
                        var diseaseName = response.disease_name;
                        var diseaseDescription = response.disease_description;
                        var diseaseCauses = response.disease_causes;
                        var diseasePrevention = response.disease_prevention;
                        var diseaseCures = response.disease_cures;

                        var uploadedImage = $('<img>');
                        uploadedImage.attr('src', imageUrl[0]);
                        uploadedImageContainer.html(uploadedImage).show();
                        uploadLabel.hide();
                        btnOuter.removeClass("file_uploading").addClass("file_uploaded");

                        // Animate text insertion
                        animateText("#plant-description", diseaseDescription);
                        animateText("#disease-cause", diseaseCauses);
                        animateText("#disease-cures", diseaseCures);
                        animateText("#disease-prevention", diseasePrevention);
                        animateText(".card-title", diseaseName);
                    } else {
                        console.error("Error: 'image_path' not found in the response.");
                        errorMessageContainer.text("Error: Image not uploaded successfully.");
                        btnOuter.removeClass("file_uploading");
                        errorOccurred = true;
                    }
                },
                error: function (xhr, status, error) {
                    processingBar.css('display', 'none');
                    errorBox.text('Error uploading image.' + error);
                    console.error("Error uploading image: " + error);
                    errorOccurred = true;
                    errorMessageContainer.text("Error uploading image. Please try again.");
                    btnOuter.removeClass("file_uploading");
                },
                complete: function () {
                    if (!errorOccurred) {
                        btnOuter.addClass("file_uploaded");
                    }
                }
            });
        }
    });

    $(".file_remove").on("click", function (e) {
        uploadedImageContainer.hide().html('');
        btnOuter.removeClass("file_uploaded");
        errorMessageContainer.text("");
        // Reset disease information in HTML elements
        resetText("#plant-description");
        resetText("#disease-cause");
        resetText("#disease-cures");
        resetText("#disease-prevention");
        resetText(".card-title");
    });

    function animateText(elementSelector, text) {
        var element = $(elementSelector);
        element.text(""); // Clear existing text
        var index = 0;
        var interval = setInterval(function () {
            element.text(element.text() + text.charAt(index));
            index++;
            if (index === text.length) {
                clearInterval(interval);
            }
        }, 50); // Adjust the interval for the desired speed
    }

    function resetText(elementSelector) {
        var element = $(elementSelector);
        element.text(""); // Clear the text
    }
})(jQuery);
