package com.example.project2;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import android.content.DialogInterface;
import android.content.Intent;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.List;

public class Workout extends AppCompatActivity {

    AlertDialog actions;
    List<String> values;
    int currentPos;
    SQLiteDatabase db = MainActivity.db;
    public final static String ITEM_INDEX2 = "com.example.project2.ITEM_INDEX2";
    public static final String TABLE_NAME = "exercises";
    public static final String COL_NAME = "name";
    public static final String COL_REPS = "reps";
    public static final String COL_SETS = "sets";
    public static final String COL_WEIGHT = "weight";
    public static final String COL_NOTES = "notes";
    final static String[] columns={"_id", COL_NAME, COL_REPS, COL_SETS, COL_WEIGHT, COL_NOTES};
    Workout hold = this;
    public final int ACTIVITY_RESULT = 1;
    public int workingIndex;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_workout);

        values = new ArrayList<>();

        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("Are you sure you want to delete this item?");
        String[] options = {"Delete"};
        builder.setItems(options,actionListener);
        builder.setNegativeButton("Cancel", null);
        actions = builder.create();

        final ListView listView = (ListView) findViewById(R.id.exerciseList);
        //add values from database to values
        Cursor result = db.query(TABLE_NAME, columns, null, null, null, null, null);
        result.moveToFirst();
        if(result.getCount() > 0){
            values.add(result.getString(1));
            while(result.moveToNext())
                values.add(result.getString(1));
        }

        final ArrayAdapter<String> adapter = new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, android.R.id.text1, values);
        listView.setAdapter(adapter);
        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
                Intent intent = new Intent(hold, Workout_exercise.class);
                intent.putExtra(ITEM_INDEX2, adapterView.getItemAtPosition(i).toString());
                workingIndex = i;
                startActivityForResult(intent, ACTIVITY_RESULT);
            }
        });
        listView.setOnItemLongClickListener(new AdapterView.OnItemLongClickListener() {
            @Override
            public boolean onItemLongClick(AdapterView<?> adapterView, View view, int i, long l) {
                currentPos = values.indexOf(((TextView) view).getText());
                actions.show();
                return true;
            }
        });
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data){
        if(resultCode == ACTIVITY_RESULT){
            values.remove(values.get(workingIndex));
            final ListView listView = (ListView) findViewById(R.id.exerciseList);
            final ArrayAdapter<String> adapter = new ArrayAdapter<String>(Workout.this, android.R.layout.simple_list_item_1, android.R.id.text1, values);
            listView.setAdapter(adapter);
        }
    }

    DialogInterface.OnClickListener actionListener = new DialogInterface.OnClickListener() {
        @Override
        public void onClick(DialogInterface dialog, int which) {
            switch (which) {
                case 0:  // Delete
                    values.remove(values.get(currentPos));
                    final ListView listView = (ListView) findViewById(R.id.exerciseList);
                    final ArrayAdapter<String> adapter = new ArrayAdapter<String>(Workout.this, android.R.layout.simple_list_item_1, android.R.id.text1, values);
                    listView.setAdapter(adapter);
                    break;
                default:
                    break;
            }
        }
    };
}
