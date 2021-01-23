package com.example.sridevivenkat.firebaseconnectivity;

import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.net.Uri;
import android.os.Environment;
import android.provider.MediaStore;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.firebase.storage.FirebaseStorage;
import com.google.firebase.storage.StorageReference;
import com.google.firebase.storage.UploadTask;

import java.io.File;

public class MainActivity extends AppCompatActivity {

   private StorageReference mStorageRef;
   private static final int RESULT_LOAD_IMAGE = 1;
   private String filePath = Environment.getExternalStorageDirectory().toString();
   Button b1;

   @Override
   protected void onCreate(Bundle savedInstanceState) {
       super.onCreate(savedInstanceState);
       setContentView(R.layout.activity_main);
       mStorageRef = FirebaseStorage.getInstance().getReference();


       b1 = (Button) findViewById(R.id.b1);

       b1.setOnClickListener(new View.OnClickListener() {
           @Override
           public void onClick(View view) {
               //Toast.makeText(MainActivity.this, "Works!!", Toast.LENGTH_SHORT).show();
               Intent intent = new Intent();
               intent.setAction(Intent.ACTION_GET_CONTENT);
               intent.setType("application/pdf");

               try {
                   startActivityForResult(intent,RESULT_LOAD_IMAGE);
               }
               catch (ActivityNotFoundException e) {

               }
           }
       });
       OcrManager manager = new OcrManager();
       manager.intitAPI();
   }

   protected void onActivityResult(int requestCode, int resultCode, Intent data) {
       switch (requestCode) {
           case 1:
               if (resultCode == RESULT_OK) {
                   // Get the Uri of the selected file
                   Uri uri = data.getData();
                   String uriString = uri.toString();
                   File myFile = new File(uriString);
                   StorageReference imageRef = mStorageRef.child("Files/uploadedFile");

                   imageRef.putFile(uri)
                           .addOnSuccessListener(new OnSuccessListener<UploadTask.TaskSnapshot>() {
                               @Override
                               public void onSuccess(UploadTask.TaskSnapshot taskSnapshot) {
                                   // Get a URL to the uploaded content
                                   Uri downloadUrl = taskSnapshot.getDownloadUrl();
                                   //Toast.makeText(MainActivity.this, "Success!" + downloadUrl.toString(), Toast.LENGTH_SHORT).show();
                               }
                           })
                           .addOnFailureListener(new OnFailureListener() {
                               @Override
                               public void onFailure(@NonNull Exception exception) {
                                   //status = false;
                                   // Handle unsuccessful uploads
                                   // ...
                                   //Toast.makeText(getApplicationContext(), "Error Here!" + exception.getMessage(), Toast.LENGTH_LONG).show();
                               }
                           });
               }

       }

   }
}

