package com.example.project2;

import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.content.ContentValues;
import android.database.sqlite.SQLiteDatabase;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

public class Setup_create extends AppCompatActivity {

    SQLiteDatabase db = MainActivity.db;
    public static final String TABLE_NAME = "exercises";
    public static final String COL_NAME = "name";
    public static final String COL_REPS = "reps";
    public static final String COL_SETS = "sets";
    public static final String COL_WEIGHT = "weight";
    public static final String COL_NOTES = "notes";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_setup_create);
    }

    public void onAddClicked(View v){
        EditText reps = (EditText) findViewById(R.id.newReps);
        EditText sets = (EditText) findViewById(R.id.newSets);
        EditText weight = (EditText) findViewById(R.id.newWeight);
        EditText notes = (EditText) findViewById(R.id.newNotes);
        EditText name = (EditText) findViewById(R.id.newName);
        String nameText = name.getText().toString();
        if(nameText.length() < 1){
            Toast.makeText(getApplicationContext(), ("Please insert a name"), Toast.LENGTH_SHORT).show();
        }
        else{
            String repsText = reps.getText().toString();
            String setsText = sets.getText().toString();
            String weightText = weight.getText().toString();
            String notesText = notes.getText().toString();
            ContentValues values = new ContentValues();
            values.put(COL_NAME,nameText);
            if(repsText.length() < 1)
                repsText = "10";
            if(setsText.length() < 1)
                setsText = "3";
            values.put(COL_REPS, repsText);
            values.put(COL_SETS, setsText);
            values.put(COL_WEIGHT, weightText);
            values.put(COL_NOTES, notesText);
            db.insert(TABLE_NAME, null, values);
            setResult(Activity.RESULT_FIRST_USER);
            finish();
        }
    }

    public void onCancelClickedNew(View v){
        finish();
    }
}
