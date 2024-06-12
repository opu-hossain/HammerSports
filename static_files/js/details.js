$(document).ready(function() {
    $('.reply-button').click(function() {
        $(this).next('.reply-form').toggle();
    });
});