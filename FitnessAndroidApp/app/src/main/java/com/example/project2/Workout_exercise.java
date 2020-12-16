package com.example.project2;

import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.content.Intent;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;

public class Workout_exercise extends AppCompatActivity {

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
        setContentView(R.layout.activity_workout_exercise);

        intent = getIntent();
        Cursor result = db.query(TABLE_NAME, columns, null, null, null, null, null);
        String stringHolder = intent.getStringExtra(Workout.ITEM_INDEX2);
        while(result.moveToNext()){
            if(result.getString(1).equals(stringHolder))
                break;
        }
        TextView t = (TextView) findViewById(R.id.exerciseName);
        t.setText(result.getString(1) + ":");
        t = (TextView) findViewById(R.id.exerciseReps);
        t.setText("Reps: " + result.getString(2));
        t = (TextView) findViewById(R.id.exerciseSets);
        t.setText("Sets: " + result.getString(3));
        t = (TextView) findViewById(R.id.exerciseWeight);
        if(result.getString(4).length() < 6)
            t.setText("Weight: " + result.getString(4));
        t = (TextView) findViewById(R.id.exerciseNotes);
        if(result.getString(5).length() > 1)
            t.setText("Notes: " + result.getString(5));
    }

    public void onCompleteClicked(View v){
        setResult(Activity.RESULT_FIRST_USER);
        finish();
    }
}
