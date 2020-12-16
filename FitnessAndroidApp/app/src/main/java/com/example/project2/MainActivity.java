package com.example.project2;

import androidx.appcompat.app.AppCompatActivity;

import android.content.ContentValues;
import android.content.Context;
import android.content.Intent;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.os.Bundle;
import android.view.View;

public class MainActivity extends AppCompatActivity {

    static SQLiteDatabase db = null;
    public static final String TABLE_NAME = "exercises";
    public static final String COL_NAME = "name";
    public static final String COL_REPS = "reps";
    public static final String COL_SETS = "sets";
    public static final String COL_WEIGHT = "weight";
    public static final String COL_NOTES = "notes";
    final static String[] columns={"_id", COL_NAME, COL_REPS, COL_SETS, COL_WEIGHT, COL_NOTES};

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        boolean dbNull = false;
        if(db == null)
            dbNull = true;
        DatabaseOpenHelper dbHelper = new DatabaseOpenHelper(this);
        db = dbHelper.getWritableDatabase();
        Cursor result = db.query(TABLE_NAME, columns, null, null, null, null, null);
        int amount = result.getCount();
        System.out.println(amount);
        if(amount < 1 &&dbNull)
            insertInitialExercises();
    }

    public void onSetupClicked(View v){
        Intent intent = new Intent(this, Setup.class);
        startActivity(intent);
    }

    public void onWorkoutClicked(View v){
        Intent intent = new Intent(this, Workout.class);
        startActivity(intent);
    }

    private void insertInitialExercises(){
        ContentValues values = new ContentValues();
        values.put(COL_NAME, "Situps");
        values.put(COL_REPS, "10");
        values.put(COL_SETS, 3);
        values.put(COL_WEIGHT, "");
        values.put(COL_NOTES, "");
        db.insert(TABLE_NAME, null, values);
        values.clear();
        values.put(COL_NAME, "Bicep Curls");
        values.put(COL_REPS, "12");
        values.put(COL_SETS, 3);
        values.put(COL_WEIGHT, 15);
        values.put(COL_NOTES, "Good form!");
        db.insert(TABLE_NAME, null, values);
        values.clear();
        values.put(COL_NAME, "Pushups");
        values.put(COL_REPS, 10);
        values.put(COL_SETS, 2);
        values.put(COL_WEIGHT, "");
        values.put(COL_NOTES, "");
        db.insert(TABLE_NAME, null, values);
    }

    public class DatabaseOpenHelper extends SQLiteOpenHelper {

        private static final int DB_VERSION = 1;
        private static final String CREATE_CMD = "CREATE TABLE " + TABLE_NAME + "(" + "_id " + "INTEGER PRIMARY KEY AUTOINCREMENT, " + COL_NAME + " VARCHAR(200) NOT NULL," + COL_REPS + " int, " + COL_SETS + " int, " + COL_WEIGHT + " int, " + COL_NOTES + " VARCHAR(200))";
        public DatabaseOpenHelper(Context context) {
            super(context,"exercises",null,1);
        }
        @Override
        public void onCreate(SQLiteDatabase db) {
            db.execSQL(CREATE_CMD);
        }
        @Override
        public void onUpgrade(SQLiteDatabase db, int oldV, int newV){
            db.execSQL("DROP TABLE IF EXISTS " + TABLE_NAME);
            onCreate(db);
        }
    }
}
