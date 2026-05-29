$(document).ready(function () {

    // -----------------------
    // فیلتر قیمت (صفحه محصولات)
    // -----------------------
    const slider = $('input[name="price"]');
    const priceDisplay = $('#sel_price');
    const form = $('#price-filter-form');

    if (slider.length && priceDisplay.length && form.length) {

        function formatNumber(value) {
            return new Intl.NumberFormat().format(value);
        }

        function updatePrice(value) {
            priceDisplay.text(formatNumber(value));
        }

        slider.on('input', function () {
            updatePrice($(this).val());
        });

        // اعمال فیلتر با submit فرم
        form.on('submit', function(e){
            e.preventDefault(); // جلوگیری از رفرش صفحه
            const priceValue = slider.val();

            $.ajax({
                type: 'GET',
                url: '/products/ajax-price-filter/', // لینک درست
                data: { price: priceValue },
                success: function(response){
                    $('#product-list').html(response);
                },
                error: function(){
                    alert('خطا در دریافت محصولات!');
                }
            });
        });

        // بازنشانی فیلتر
        $('#reset-filter').on('click', function(){
            slider.val(slider.attr('max'));
            updatePrice(slider.val());
            form.submit();
        });

        updatePrice(slider.val());
    }

    // -----------------------
    // فیلتر ویژگی‌ها (Admin Inline)
    // -----------------------
    $(document).on('change', 'select[id^="id_product_features-"][id$="-feature"]', function() {
        const featureId = $(this).val();           // id ویژگی
        const dd1 = $(this).attr('id');            // مثل id_product_features-0-feature
        const dd2 = dd1.replace("-feature", "-filter_value"); // id مربوط به filter_value

        $.ajax({
            type: "GET",
            url: "/products/ajax-admin/",
            data: { feature_id: featureId },
            success: function(res) {
                const cols = document.getElementById(dd2);
                if (!cols) return;  // اگر هنوز row ساخته نشده
                cols.options.length = 0;  // پاک کردن مقادیر قبلی

                // اضافه کردن گزینه‌های جدید
                for (const k in res) {
                    if (res.hasOwnProperty(k)) {
                        cols.options.add(new Option(k, res[k]));
                    }
                }
            },
            error: function() {
                console.error("خطا در دریافت مقادیر ویژگی!");
            }
        });
    });

});

