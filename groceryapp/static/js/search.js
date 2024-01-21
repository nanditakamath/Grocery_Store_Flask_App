$(document).ready(function () {
    var $searchButton = $('#searchButton');

    $searchButton.on('click', function () {
        var searchText = $('#searchInput').val().trim();
        if (searchText !== '') {
            if (window.find(searchText)) {
                document.execCommand('hiliteColor', false, 'yellow'); // Highlight the found text
            } else {
                alert('Text not found');
            }
        }
    });
});
