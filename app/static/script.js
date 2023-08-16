$(document).ready(function () {
  const userRegistrationForm = $("#user_register_form");
  const userLoginForm = $("#user_login_form");
  const userRegistrationFormContainer = $("#register_form_container");
  const userLoginFormContainer = $("#login_form_container");
  const userRegisterFormButton = $("#user_register_form_button");
  const userLoginFormButton = $("#user_login_form_button");
  const showUserLoginForm = $("#show_login_form");
  const showUserRegisterForm = $("#show_register_form");
  const USER_REGISTER_URL = "/register";
  const USER_LOGIN_URL = "/login";
  const USER_LOGOUT_URL = "/logout";

  showUserLoginForm.click(function (e) {
    console.log("Login form link clicked");
    e.preventDefault();
    userRegistrationFormContainer.hide();
    userLoginFormContainer.show();
  });

  showUserRegisterForm.click(function (e) {
    console.log("Register form link clicked");
    e.preventDefault();
    userLoginFormContainer.hide();
    userRegistrationFormContainer.show();
  });

  function handleFormSubmission(e, form, url) {
    e.preventDefault();
    //  serializes input data into an array where each item is an object representing a form field.
    let formDataArray = form.serializeArray();
    console.log(formDataArray);
    let formDataObj = {};

    $(formDataArray).each(function (index, obj) {
      formDataObj[obj.name] = obj.value;
    });

    console.log(formDataObj);

    $.ajax({
      type: "POST",
      url: url,
      contentType: "application/json;charset=UTF-8",
      data: JSON.stringify(formDataObj),
      success: function (data) {
        location.reload();
        $("#content_block_container").html(`<h1>${data.message}!</h1>`);
      },
      error: function (error) {
        alert(error.responseText);
      },
    });
  }

  userRegisterFormButton.click(function (e) {
    handleFormSubmission(e, userRegistrationForm, USER_REGISTER_URL);
  });

  userLoginFormButton.click(function (e) {
    handleFormSubmission(e, userLoginForm, USER_LOGIN_URL);
  });
});

$("#logoutButton").click(function (e) {
  e.preventDefault();

  $.ajax({
    type: "POST",
    url: "/logout",
    success: function (data) {
      window.location.href = "/";
    },
    error: function (error) {
      alert(error.responseText);
    },
  });
});

// AJAX Request test
// userRegisterFormButton.click(function (e) {
//   e.preventDefault();
//   let form = $("#user_register_form");
//   let formDataArray = form.serializeArray();
//   let formDataObj = {};

//   $(formDataArray).each(function (index, obj) {
//     formDataObj[obj.name] = obj.value;
//   });

//   console.log(formDataObj);

//   $.ajax({
//     type: "POST",
//     url: "http://127.0.0.1:5000/register",
//     contentType: "application/json;charset=UTF-8",
//     data: JSON.stringify(formDataObj),
//   });
// });