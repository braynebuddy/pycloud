// Search Function
//
// from - https://www.geeksforgeeks.org/live-search-using-flask-and-jquery/
//
jQuery(document).ready(function($){
  
    $('.tagcloud li').each(function(){
        $(this).attr('search-term', $(this).text().toLowerCase());
    });
    $('.search-list').each(function(){
        $(this).attr('search-term', $(this).text().toLowerCase());
    });
      
    $('.search-box').on('keyup', function(){
        var searchTerm = $(this).val().toLowerCase();
        $('.tagcloud li').each(function(){
            if ($(this).filter('[search-term *= ' + searchTerm + ']').length > 0 || searchTerm.length < 1) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
        $('.search-list').each(function(){
            if ($(this).filter('[search-term *= ' + searchTerm + ']').length > 0 || searchTerm.length < 1) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });
});