$(document).ready(function () {
    const slider = $('#price-slider');
    const currentPriceHeader = $('#current-price-header');
    const priceForm = $('#price-filter-form');

    function formatNumber(value) {
        return new Intl.NumberFormat().format(value);
    }

    function updateCurrentPrice(value) {
        currentPriceHeader.text(formatNumber(value) + " تومان");
    }

    // مقدار اولیه
    updateCurrentPrice(slider.val());

    // آپدیت وقتی اسلایدر حرکت می‌کنه
    slider.on('input', function() {
        updateCurrentPrice(this.value);
    });

    // اعمال فیلتر با AJAX
    priceForm.on('submit', function(e) {
        e.preventDefault();
        const priceValue = slider.val();

        $.ajax({
            type: 'GET',
            url: '/products/ajax-price-filter/',
            data: { price: priceValue },
            success: function(response){
                $('#product-list').html(response);
            },
            error: function(){
                alert('خطا در دریافت محصولات!');
            }
        });
    });

    // بازنشانی
    $('#reset-filter').on('click', function() {
        slider.val(slider.attr('max'));
        updateCurrentPrice(slider.val());
        priceForm.submit();
    });
});


// تابع حذف پارامترهای خط آدرس
function removeURLParameter(url, parameter) {
    var urlparts = url.split('?');
    if (urlparts.length >= 2){
        var prefix = encodeURIComponent(parameter) + '='
        var pars = urlparts[1].split(/[&;]/g);
        for (var i = pars.length; i-- > 0;) {
            if (pars[i].lastIndexOf(prefix, 0) !== -1) {
                pars.splice(i, 1);
            }
        }
        return urlparts[0] + (pars.length > 0 ? '?' + pars.join('&') : '');
    }
    return url;
}


// تابع انتخاب مدل مرتب سازی محصول
function select_sort() {
    var select_sort_value = $('#select_sort').val();
    var baseUrl = window.location.origin + window.location.pathname;
    var params = new URLSearchParams(window.location.search);
    params.set('sort_type', select_sort_value);  // اگر بود آپدیت می‌کند، اگر نبود اضافه می‌کند
    window.location.href = baseUrl + '?' + params.toString();
}

// تابع فیلتر نمابش بر اساس تعداد
function select_count() {
    var count_value = $('#select_count').val();
    var baseUrl = window.location.origin + window.location.pathname;
    var params = new URLSearchParams(window.location.search);
    params.set('count', count_value);
    params.delete('page');    // اگر صفحه فعلی پارامتر page دارد، بهتر است حذفش کنیم تا از صفحه اول شروع شود
    window.location.href = baseUrl + '?' + params.toString();
}


// سبد خرید
function status_of_shop_cart() {
    $.ajax({
        type:"GET",
        url:"/orders/status-of-shop-cart/",
        success: function(res) {
            $("#indicator__value").text(res.count);
        }
    });
}

status_of_shop_cart();



function add_to_shop_cart(product_id, qty) {
    if (qty == 0) {
        qty = $("#product-quantity").val();
    }
    $.ajax({
        type:"GET",
        url:"/orders/add-to-shop-cart/",
        data: {
            product_id: product_id,
            qty: qty
        },
        success: function(res) {
            console.log("کالای مورد نظر به سبد خرید شما اضافه شد", res);
            status_of_shop_cart();
        }
    });
}



function delete_from_shop_cart(product_id) {
    if(confirm("حذف شود؟")) {
        $.ajax({
            type:"GET",
            url:"/orders/delete-from-shop-cart/",
            data:{
                product_id:product_id
            },
            success: function(res) {
                $("#shop_cart_list").html(res);
                status_of_shop_cart();
            }
        });
    }
}



// این تابع برای اینه که تو قسمت سبد خرید دوتا لیست درست میکنم یه لیست آیدیه محصولات توش باشه یه لیست تعداد محصولات فعلی توش باشه
function update_shop_cart() {
    var product_id_list = [];
    var qty_list = [];  // ✅

    $("input[id^='qty_']").each(function() {
        var id = $(this).attr('id');  // qty_21
        var product_id = id.slice(4);  // 21 ✅
        if (product_id) {
            product_id_list.push(product_id);
            qty_list.push($(this).val());
        }
    });

    $.ajax({
        type: "GET",
        url: "/orders/update-shop-cart/",
        data: {
            'product_id_list[]': product_id_list,
            'qty_list[]': qty_list
        },
        success: function(res) {
            location.reload();  // ✅ partial آپدیت
            status_of_shop_cart();           // ✅ شمارنده
        }
    });
}



function showCreateCommentForm(productId, commentId, slug) {
    $.ajax({
        type: "GET",
        url: "/csf/create-comment/" + slug + "/?productId=" + productId + "&commentId=" + commentId,
        success: function(res) {
            $("#btn_" + commentId).hide();
            $("#comment_form_" + commentId).html(res);
        },
        error: function(xhr) {
            console.log("خطا:", xhr.responseText);
        }
    });
}


// تابع برای امتیاز دهی و بدست آوردن میانگین امتیاز یه کالایی و اونو بصورت ایجکس آپدیت کنه
function addScore(score, productId) {
    const starRatings = document.querySelectorAll(".fa-star");
    starRatings.forEach(el => el.classList.remove("checked"));
for (let i = 1; i <= score; i++) {
        const element = document.getElementById("star_" + i);
        if (element) element.classList.add("checked");
    }
$.ajax({
        type: "GET",
        url: "/csf/add-score/",
        data: {
            productId: productId,
            score: score,
        },
        success: function(res) {
            alert("امتیاز با موفقیت ثبت شد");
        },
        error: function(xhr, status, error) {
            alert("خطا در ثبت امتیاز: " + error);
        }
    });
// غیرفعال کردن ستاره‌ها پس از ثبت
    starRatings.forEach(el => el.classList.add("disable"));
}


// تابع ایجکسی برای قلب پایین عکس کالا توی باکس
$(document).on('click', '.product-card__wishlist', function(e) {
    e.preventDefault();
    const productId = $(this).data('product');
    const btn = this;

    $.ajax({
        type: "GET",
        url: "/csf/add-to-favorite/",
        data: { productId: productId },
        success: function(res) {
            console.log(res);

            if (res.includes('اضافه شد')) {
                $(btn).html(`
                    <i class="fa fa-heart text-danger"></i>
                    <span class="fake-svg-icon fake-svg-icon--wishlist-16"></span>
                `);
                $(btn).addClass('favorited');
            } else {
                $(btn).html(`
                    <i class="fa fa-heart-broken"></i>
                    <span class="fake-svg-icon fake-svg-icon--wishlist-16"></span>
                `);
                $(btn).removeClass('favorited');
            }
        }
    });
});


//این تابع وضعیت لیست مقایسه کالا رو نوشن میده
function status_of_compare_list() {
    $.ajax({
        type:"GET",
        url: "/products/status-of-compare-list/",
        success: function(res) {
            if (Number(res) === 0) {
                $("#compare_count_icon").hide();
            } else {
                $("#compare_count_icon").show();
                $("#compare_count").text(res)
            }
        }
    });
}



function addToCompareList(productId, productGroupId) {
    $.ajax({
        type: "GET",
        url: "/products/add-to-compare-list/",
        data: {
            productId: productId,
            productGroupId: productGroupId
        },
        success: function(res) {
        alert(res);
        status_of_compare_list();
        }
    });
}



function deleteFromCompareList(productId) {
    $.ajax({
        type: "GET",
        url: "/products/delete-from-compare-list/",
        data: {
            productId: productId,
        },
        success: function(res) {
            alert('حذف با موفقیت انجام شد');
            $("#compare_list").html(res);
            status_of_compare_list()
        }
    });
}



$('.nav-links__item--with-submenu').hover(
    function() {
        $(this).find('.fa-angle-down').css({
            'transform': 'rotate(180deg)',
            'transition': 'all 0.3s ease',
            'color': '#ff4757'
        });
    },
    function() {
        $(this).find('.fa-angle-down').css({
            'transform': 'rotate(0deg)',
            'color': 'inherit'
        });
    }
);


$(document).ready(function(){
    $('.hero-slider').owlCarousel({
        rtl: true,
        items: 1,
        loop: true,
        autoplay: true,
        autoplayTimeout: 3000,
        autoplayHoverPause: true,
        smartSpeed: 1000,
        nav: true,
        navText: ["<", ">"],
        autoHeight: false, // این باید حتما false باشد تا ارتفاع ما اعمال شود
        onInitialized: setHeight,
        onResized: setHeight
    });

    function setHeight() {
        $('.hero-slider, .hero-slider .owl-stage-outer, .hero-slider .owl-stage, .hero-slider .owl-item').css('height', '500px');
    }
});




