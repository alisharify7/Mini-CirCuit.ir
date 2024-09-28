// loading animation module js

function createAnimationElement(){
    const loaderAnimation = document.createElement('div');
    loaderAnimation.id = 'loader-animation';
    loaderAnimation.classList.add('position-fixed', 'top-0', 'd-flex', 'justify-content-center', 'align-items-center', 'w-100', 'h-100', 'bg-dark-hell');
    loaderAnimation.style.zIndex = 65000;

    const div = document.createElement("div")
    div.className = "w-100 h-100 d-flex flex-column justify-content-center align-items-center"
    div.innerHTML = `
    <div class="wrapper w-100">
        <svg>
            <text x="50%" y="50%" dy=".35em" text-anchor="middle" class="display-1">
            MiniCircuits.ir
            </text>
        </svg>
    </div>
    <p class="text-center persian-font text-white">در حال بارگذاری صفحه مورد ...</p>
    `
    loaderAnimation.appendChild(div)
    return loaderAnimation
}


// Loading Page
function ShowLoadingPageAnimation(duration = 1750) {
    const animationElement = createAnimationElement();
    document.body.appendChild(animationElement)
    window.setTimeout((e)=>{
            animationElement.remove();
    }, duration)
}

