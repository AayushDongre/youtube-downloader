$(document).ready(function(){

    console.log("aaaaaaaaaaaa")
    
    $(".download-button").click(function(e){
        
        
        // e.preventDefault()
        
        formData = new FormData(document.querySelector("#mainForm"))


        urlValue = $("#mainForm").serializeArray()[0]["value"] 
        if(urlValue.includes("youtube") && urlValue)
        {
            $(".hangOn").css("display","block");

            if(urlValue.includes("playlist")){
                $(".memes").css("display","block");
            }

            $(".notYoutubeAlert").css("display", "none")
            $.get("/download", { url:urlValue })
        
        }else{
            e.preventDefault();
            $(".hangOn").css("display","none");
            $(".memes").css("display","none");
            $(".notYoutubeAlert").css("display", "block")
        }



        
        

    })
})