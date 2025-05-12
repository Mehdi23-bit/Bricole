input=document.getElementById('search-bar')
input.addEventListener('change',(e)=>{
    input_value=input.value
    const csrf_token= '{{ csrf_token }}'
    console.log(getCSRFToken())
  fetch('http://127.0.0.1:8000/search_filter/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken()
    },
    body: JSON.stringify({ search_key: input_value })
})
.then(response => response.json())
.then(data => {
    // Hide loading spinner

    if (data.services && data.services.length > 0) {
        // Append new services
        const container = document.getElementById('services-container');
        container.replaceChildren()
        data.services.forEach((service, index) => {
            const serviceDiv = document.createElement('div');
            serviceDiv.className = 'service col-md-3 mb-4 service-fade-in';
            serviceDiv.style.animationDelay = `${index * 0.1}s`;
            serviceDiv.innerHTML = `
                <div class="card service-card h-100">
                    <div class="service-image-container">
                        <img src="${service.image}" alt="${service.title}" class="service-image">
                    </div>
                    <div class="card-body">
                        <h2 class="service-title">${service.title}</h2>
                        <p class="service-description">${service.description}</p>
                         <p class="service-description">${service.categorie}</p>
                    </div>
                </div>
            `;
            container.appendChild(serviceDiv);
        });
}
})
})

document.addEventListener('DOMContentLoaded',function(){
  input.dispatchEvent(new Event('change', { bubbles: true }));
})

function getCSRFToken() {
    const name = 'csrftoken';
    let cookieValue = null;
    
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }