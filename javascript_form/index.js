form.onsubmit = async (e) => {
    e.preventDefault();
    let formData = new FormData(form);
    let data = JSON.stringify(Object.fromEntries(formData));
    // var xhr = new XMLHttpRequest();
    // var url = 'http://localhost:4000/PostedData';
    // xhr.open("POST", url, true);
    // xhr.setRequestHeader("Content-Type", "application/json");
    // // let response = await fetch('http://localhost:4000/PostedData', {
    // //     method: 'POST',
    // //     body: new FormData(form)
    // //   });
  
    // //   let result = await response.json();
  
    // //   alert(result.message);
    // xhr.send(data);    
    // httpGet()
    console.log(httpGet('http://localhost:4000/SearchKeywords/MAAZGOLI'));
};
function httpGet(theUrl) {
    let xmlHttpReq = new XMLHttpRequest();
    xmlHttpReq.open("GET", theUrl, false); 
    xmlHttpReq.send(null);
    return xmlHttpReq.responseText;
  }
