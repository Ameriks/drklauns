django.jQuery( document ).ready(function() {
    django.jQuery("#id_start_0").change(function() {
      django.jQuery("#id_end_0").val(this.value);
    });
});
