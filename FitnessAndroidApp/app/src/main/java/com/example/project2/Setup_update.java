package com.example.project2;

import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.content.ContentValues;
import android.content.Intent;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;

import java.util.Set;

public class Setup_update extends AppCompatActivity {

    SQLiteDatabase db = MainActivity.db;
    public static final String TABLE_NAME = "exercises";
    public static final String COL_NAME = "name";
    public static final String COL_REPS = "reps";
    public static final String COL_SETS = "sets";
    public static final String COL_WEIGHT = "weight";
    public static final String COL_NOTES = "notes";
    final static String[] columns={"_id", COL_NAME, COL_REPS, COL_SETS, COL_WEIGHT, COL_NOTES};
    Intent intent;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_setup_update);

        intent = getIntent();
        Cursor result = db.query(TABLE_NAME, columns, null, null, null, null, null);
        int numberHolder = Integer.parseInt(intent.getStringExtra(Setup.ITEM_INDEX));
        result.moveToPosition(numberHolder);

        TextView updateTitle = (TextView) findViewById(R.id.updateTitle);
        updateTitle.setText("Update values for " + result.getString(1));
        updateTitle = (TextView) findViewById(R.id.name);
        updateTitle.setText("Name: " + result.getString(1));

        EditText e = (EditText) findViewById(R.id.reps);
        e.setHint(result.getString(2));

        e = (EditText) findViewById(R.id.sets);
        e.setHint(result.getString(3));

        e = (EditText) findViewById(R.id.weight);
        if(result.getString(4).length() < 1)
            e.setHint("Weight?");
        else
            e.setHint(result.getString(4));

        e = (EditText) findViewById(R.id.notes);
        e.setHint(result.getString(5));
    }

    public void onUpdateExerciseClicked(View v){
        EditText reps = (EditText) findViewById(R.id.reps);
        EditText sets = (EditText) findViewById(R.id.sets);
        EditText weight = (EditText) findViewById(R.id.weight);
        EditText notes = (EditText) findViewById(R.id.notes);
        String repsText = reps.getText().toString();
        if(repsText.length() < 1)
            repsText = reps.getHint().toString();
        String setsText = sets.getText().toString();
        if(setsText.length() < 1)
            setsText = sets.getHint().toString();
        String weightText = weight.getText().toString();
        if(weightText.length() < 1)
            if(weightText != "Weight?")
                weightText = weight.getHint().toString();
        String notesText = notes.getText().toString();
        if(notesText.length() < 1)
            notesText = notes.getHint().toString();

        Cursor result = db.query(TABLE_NAME, columns, null, null, null, null, null);
        int numberHolder = Integer.parseInt(intent.getStringExtra(Setup.ITEM_INDEX));
        result.moveToPosition(numberHolder);
        String name = result.getString(1);
        db.delete(TABLE_NAME, "name =?", new String[]{result.getString(1)});
        ContentValues values = new ContentValues();
        values.put(COL_NAME, name);
        values.put(COL_REPS, repsText);
        values.put(COL_SETS, setsText);
        values.put(COL_WEIGHT, weightText);
        values.put(COL_NOTES, notesText);
        db.insert(TABLE_NAME, null, values);
        setResult(Activity.RESULT_FIRST_USER);
        finish();
    }

    public void onCancelClicked(View v){
        finish();
    }
}
