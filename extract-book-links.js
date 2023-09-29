// Open https://www.livelib.ru/reader/username/read/print page in browser, go to devtools, run the script
// Get all anchor tags in the document
var links = document.querySelectorAll('a');

// Filter links that start with "/book/"
var bookLinks = Array.from(links).filter(link => link.getAttribute('href').startsWith('/book/'));

// Extract href attribute from each link
var bookLinksHref = bookLinks.map(link => link.href);

// Create a blob from the links and create a link element to download it
var blob = new Blob([bookLinksHref.join('\n')], { type: 'text/plain' });
var link = document.createElement('a');
link.href = window.URL.createObjectURL(blob);
link.download = 'book-links.txt';

// Append the link to the document, trigger the download and remove the link
document.body.appendChild(link);
link.click();
document.body.removeChild(link);