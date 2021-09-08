$( document ).on( 'click', '.details a', function(event) {
   if (event.target.hasAttribute('href')) {
       var link = event.target.href + 'ajax/';
       var link_array = link.split('/');
       alert(link_array);
       alert(link_array[4]);
       if (link_array[4] == 'category') {
           $.ajax({
               url: link,
               success: function (data) {
                   $('.details').html(data.result);
               },
           });

           event.preventDefault();
       }
   }
});
