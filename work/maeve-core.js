if( "function" != typeof load_Morenvy_BannerManagerScript )
    {
        function load_Morenvy_BannerManagerScript( useCache, path )
        {
            let styleTag = "<style>.morenvy-banner-area:not(.init){display:none !important;}</style>";
            document.write( styleTag );

            styleTag = "<style>.morenvy-product-area:not(.init){display:none !important;}</style>";
            document.write( styleTag );

            let scriptTag = "";
            if( true == useCache )
                scriptTag = "<script src=" + path + "><\/script>";
            else
                scriptTag = "<script src=" + path + "?v=" + Date.now() + "><\/script>";
            document.write( scriptTag );
        }
    }