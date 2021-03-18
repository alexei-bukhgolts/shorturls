function successMessage(message) {
    return  '<div class="alert alert-success">' +
            '<button type="button" class="close" data-dismiss="alert">' +
            '&times;</button>' + message + '</div>';
}

function errorMessage(message) {
    return  '<div class="alert alert-danger">' +
            '<button type="button" class="close" data-dismiss="alert">' +
            '&times;</button>' + message + '</div>';
}

function getErrorMessageByServerResponse(responseText) {
    const errorsObj = JSON.parse(responseText.replace("shortUrl", "subpart")); // kinda dirty hack, but I'm not a frontend developer
    let errorMessageString = "";
    Object.entries(errorsObj).forEach(([key, value]) => {
        switch (key) {
            case "shortUrl":
                errorMessageString += `"Subpart in our domain" - ${value}; `
                break;
            case "longUrl":
                errorMessageString += `"Full target URL" - ${value}; `
                break;
            default:
                errorMessageString += `${key} - ${value}`
                break;
        }
    })
    return errorMessageString;
}

$(function() {
    $("#formPostRedirect").on("submit", function(e) {
        e.preventDefault();
        $.ajax({
            url: $(this).attr("action"),
            type: 'POST',
            data: $(this).serialize(),
            beforeSend: function() {
            },
            error: (jqXHR, error, errorThrown) =>
                !error ?
                    $("#alerts").append(errorMessage(`Request failed, could not deliver to server`)):
                    $("#alerts").append(errorMessage(`Request failed: ${error}, ${errorThrown}, ${getErrorMessageByServerResponse(jqXHR.responseText)}`)),
            success: function(data) {
            },
            statusCode: {
                201: () => $("#alerts").append(successMessage("Redirect created successfully!")),
            }
        });
    });
});