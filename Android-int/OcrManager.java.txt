package com.example.sridevivenkat.firebaseconnectivity;

import android.graphics.Bitmap;

import com.googlecode.tesseract.android.TessBaseAPI;

/**
* Created by sridevi venkat on 3/7/2019.
*/

public class OcrManager {
   TessBaseAPI baseAPI = null;
   public void intitAPI(){
       baseAPI= new TessBaseAPI();
       String dataPath = MainApplication.instance.getTessDataParentDirectory();
       baseAPI.init(dataPath,"eng");
   }
   public String startRecognize(Bitmap bitmap)
   {
       if(baseAPI ==null)
           intitAPI();
       baseAPI.setImage(bitmap);
       return baseAPI.getUTF8Text();
   }
}
