
document.querySelector('#hamburger-button').addEventListener('click', function() {
    document.getElementById('mobile-menu').classList.toggle('hidden');
});

var dropdownMenu = document.getElementById('dropdown-menu');
var accountIcon = document.getElementById('account-icon');

// Search section dropdown
var searchDropdown = document.getElementById('search-dropdown');
var searchIcon = document.getElementById('search-icon');

// Account section dropdown
if (accountIcon) {
    accountIcon.addEventListener('click', function(event) {
        event.stopPropagation();
        if (dropdownMenu.classList.contains('hidden')) {
            dropdownMenu.classList.remove('hidden');
            // Hide the search dropdown when the account dropdown is shown
            if (!searchDropdown.classList.contains('hidden')) {
                searchDropdown.classList.add('hidden');
            }
        } else {
            dropdownMenu.classList.add('hidden');
        }
    });
}

document.addEventListener('click', function() {
    if (!dropdownMenu.classList.contains('hidden')) {
        dropdownMenu.classList.add('hidden');
    }
});

if (searchIcon) {
    searchIcon.addEventListener('click', function(event) {
        event.stopPropagation();
        if (searchDropdown.classList.contains('hidden')) {
            searchDropdown.classList.remove('hidden');
            // Hide the account dropdown when the search dropdown is shown
            if (!dropdownMenu.classList.contains('hidden')) {
                dropdownMenu.classList.add('hidden');
            }
        } else {
            searchDropdown.classList.add('hidden');
        }
    });
}

// Hide search dropdown when clicking anywhere on the page
document.addEventListener('click', function() {
    if (!searchDropdown.classList.contains('hidden')) {
        searchDropdown.classList.add('hidden');
    }
});

// Prevent dropdown from being hidden when the search form is clicked
var searchForm = document.querySelector('#search-dropdown form');
if (searchForm) {
    searchForm.addEventListener('click', function(event) {
        event.stopPropagation();
    });
}
