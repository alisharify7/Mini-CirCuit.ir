// global js
// @auther:  github.com/alisharify7
const burger_menu = document.querySelector("#navbar-burger-menu");
if (burger_menu) {
    burger_menu.addEventListener("click", function (e) {
        burger_menu.classList.toggle("burger_active");
    });
}
const footer_wavy = document.querySelector(".footer-social-container")
if (footer_wavy){
    rem = 10
    let template = `  --mask:
    radial-gradient(${rem}em at 50% 15em,#000 99%,#0000 101%) calc(50% - 10em) 0/20em 100%,
    radial-gradient(${rem}em at 50% -10em,#0000 99%,#000 101%) 50% 5em/20em 100% repeat-x;
  -webkit-mask: var(--mask);
          mask: var(--mask);`
    window.setInterval( e=>{
        footer_wavy.style = template;
        rem += 1
    }, 1000)
}

console.log(`
                             _    _     _           
__ __ _____   __ _ _ _ ___  | |_ (_)_ _(_)_ _  __ _ 
\\ V  V / -_) / _\` | '_/ -_) | ' \\| | '_| | ' \\/ _\` |
 \\_/\\_/\\___| \\__,_|_| \\___| |_||_|_|_| |_|_||_\\__, |
                                              |___/ 
-> hire@minicircuits.ir <-

`)

const partnership_owl = $(".partnership-company-slider");
if (partnership_owl) {
    partnership_owl.owlCarousel({
        rtl: true,
        loop: true,
        margin: 10,
        autoplay: true,
        responsiveClass: true,
        autoplayTimeout: 600,
        autoplayHoverPause: true,
        lazyLoad: true,
        center: true,
        nav: false,
        dots: false,
        pagination: false,
        navigation: false,
        responsive: {
            0: {
                items: 2,
            },
            400: {
                items: 3,
            },
            980: {
                items: 6,
            },
            1400: {
                items: 7,
            },
        },
        navText: ["<i class='bi bi-chevron-right display-4 fw-bold mt-3 '></i>", "<i class='bi bi-chevron-left display-4 fw-bold mt-3 '></i>"]

    });
}

