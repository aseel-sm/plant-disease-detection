$(document).ready(function () {
  $("#loading").show();
  $("#imageWidget").hide();
  $("#prediction-container").hide();
  $("#predict-btn").hide();
  $("#new-btn").hide();
  $("#prediction-widget").hide();
  $("#remedy-list").hide();

  function getFileUrl(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();
      reader.onload = function (e) {
        $("#imageWidget").attr("src", e.target.result);
      };
      reader.readAsDataURL(input.files[0]);
    }
  }
  $("#new-btn").click(function () {
    location.reload();
  });
  $("#image-input").change(function () {
    getFileUrl(this);
    $("#imageWidget").show();
    $("#predict-btn").show();
  });
  $("#predict-btn").click(() => {
    $("#loading").show();
    $("#prediction-widget").show();
    let uploadedImage = new FormData($("#upload-form")[0]);

    $.ajax({
      type: "POST",
      url: "/predict",
      data: uploadedImage,
      contentType: false,
      cache: false,
      processData: false,
      async: true,
      success: function (data) {
        // Get and display the result

        if (data["remedy"] == "NIL") {
          $("#prediction-container").addClass("bg-success");
          $("#remedy-list").append(
            "<li class='list-group-item'>Healthy Leaf🙂 </li>"
          );
        } else {
          $("#prediction-container").addClass("bg-danger");
          remedy = data["remedy"][0];
          remedy_link = data["remedy"][1];
          for (let i = 0; i < data["remedy"][0].length; i++) {
            $("#remedy-list").append(
              " <li class='list-group-item'>" +
                "<a href=" +
                remedy_link[i] +
                " target='_blank'>" +
                remedy[i] +
                "</a>" +
                "</li>"
            );
          }
        }
        $("#loading").hide();
        $("#prediction-container").text(data["disease"]);

        $("#prediction-container").show();

        $("#prediction-widget").show();
        $("#remedy-list").show();
        $("#predict-btn").hide();
        $("#new-btn").show();
        console.log(data);
        console.log("Success!");
      },
    });
  });
});
