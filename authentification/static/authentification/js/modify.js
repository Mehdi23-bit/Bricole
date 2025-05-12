/*******************************************/
/*                                         */        
/*               Functions                 */
/*                                         */
/*******************************************/

async function retrieve_file(url, input,File_list) {
    if (input.files.length > 0) return;
    
    try {
        const response = await fetch(url);
        if (response.ok) {
            const blob = await response.blob();
            let file = new File([blob], `${generate_random_str()}.png`);
            array=Object.values(File_list)
            const dataTransfer = new DataTransfer();
            array.forEach(element=>{
                dataTransfer.items.add(element);
            });
            dataTransfer.items.add(file)
            File_list[file.name]=file
            input.files = dataTransfer.files;
        }
    } catch (error) {
        console.log(error);
    }
}

function generate_random_str() {
    let result = '';
    const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    for (let i = 0; i < 20; i++) {
        const nbr = Math.trunc(Math.random() * 100) % chars.length;
        result += chars.charAt(nbr);
    }
    return result;
}

function refreshEventListener() {
    document.getElementsByName('delete').forEach(element => {
        element.addEventListener('click', (e) => {
            deleteElemFromInput(element.id, document.getElementById("input_images"));
            element.parentElement.remove();
        });
    });
}

function load_imgs(input) {
    console.log("i am loading pictures")
    let img_div = document.getElementById('images');
    let images_array = Object.values(input)
    let html = '';
    img_div.innerHTML=''
    images_array.forEach((elem, i) => {
        console.log("picture ")
        const image_url = URL.createObjectURL(elem);
        html += `
        <div>
            <span name='delete' style='background-color:Red;' id='${elem.name}'>delete</span>
            <img src="${image_url}" width="300" height="300">
        </div>`;
    });

    img_div.insertAdjacentHTML('beforeend', html);
    refreshEventListener();
}

function deleteElemFromInput(index, input) {
      let dataTransfer=new DataTransfer() 
      delete File_list[index]
      for (let key in File_list) {
        console.log("i am deleting")
        dataTransfer.items.add(File_list[key]);
      }
      input.files=dataTransfer.files
    }

function copyFiles(input, fileList) {
    let input_array = Array.from(input.files);
    let file_list_array = Object.values(fileList);
    let dataTransfer = new DataTransfer();

    input_array.forEach(element => {
        console.log("copy input")
        fileList[element.name]=element
        dataTransfer.items.add(element);
    });

    file_list_array.forEach(element => {
        console.log("copy files list")
        dataTransfer.items.add(element);
    });

    
    input.files = dataTransfer.files;
    return fileList
    console.log("data transfer is "+fileList)
}

/*************************************/
/*                                   */        
/*               Main                */
/*                                   */
/*************************************/

let File_list = {};
window.addEventListener("load", (event) => {
    console.log("loading window");
    
    Array.from(document.getElementById("input_images").files).forEach(elem=>{
        console.log(elem.name)
        File_list[elem.name]=elem 
    })
    load_imgs(File_list)
});
document.getElementById("add").addEventListener('click',e=>{
    e.preventDefault();
    document.getElementById("input_images").click();})
let input_files = document.getElementById('input_images');
let images = document.getElementById('images');

input_files.addEventListener("change", (e) => {
    console.log("I am changing");
    File_list=copyFiles(document.getElementById('input_images'), File_list);
    console.log(document.getElementById('input_images').files);
    load_imgs(File_list);
});

const promise = new Promise(function(resolve, reject) {
    setTimeout(() => {
        resolve("done");
    }, 4000);
});

promise.then(function(resolve) {
    load_imgs(File_list);
    document.getElementById("loading").style.display = "none";
    document.getElementById("main").style.display = "block";
});
