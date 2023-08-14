const userRegisterFormButton = $("#user_register_form_button");

console.log(userRegisterFormButton);
userRegisterFormButton.click(function (e) {
  e.preventDefault();
  let form = $("#user_register_form");
  let url = form.prop("action");
  let type = form.prop("method");
  let formData = form.serialize();

  console.log(url, type, formData);
  $.ajax({
    type: "POST",
    url: "/test_register",
    contentType: "application/json;charset=UTF-8",
    data: formData,
  });
});
