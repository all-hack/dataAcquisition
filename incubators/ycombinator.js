var arr = $('.name').children()
arr.map(function(e) { console.log(arr[e]['href'] + " || " + arr[e]['innerText']); })

console.log("now save this to a file and parse it with python")