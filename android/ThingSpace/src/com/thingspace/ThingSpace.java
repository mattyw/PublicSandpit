package com.thingspace;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import android.app.Activity;
import android.app.ProgressDialog;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

public class ThingSpace extends Activity {
	public class FeedData {
		public FeedData(String name, double data) {
			feedName = name;
			last_data = data;
		}
		public String feedName;
		public double last_data;
	}
	TextView responseView;
	Button update;
	EditText channel;
	ProgressDialog progress;
	
	final Handler mHandler = new Handler();
	FeedData mFD = new FeedData("m", 0);
	final Runnable mUpdateResults = new Runnable() {
		public void run() {
			updateResults();
		}
	};
	final Runnable mStartProgressBar = new Runnable() {
		public void run() {
			startProgressBar();
		}
	};
	final Runnable mStopProgressBar = new Runnable() {
		public void run() {
			stopProgressBar();
		}
	};
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        responseView = (TextView)findViewById(R.id.response);
        channel = (EditText)findViewById(R.id.channel);
        update = (Button)findViewById(R.id.update);
        progress = new ProgressDialog(this);
        
        
        update.setOnClickListener(new View.OnClickListener() {	
			@Override
			public void onClick(View v) {
				Thread t = new Thread() {
					public void run() {
						mHandler.post(mStartProgressBar);
						mFD = sendRequest();
						mHandler.post(mUpdateResults);
						mHandler.post(mStopProgressBar);
					}
				};
				t.start();	
			}
		});
    }
    
    protected void updateResults() {
		StringBuilder sb = new StringBuilder();
		sb.append("Channel Name: " + mFD.feedName + "\n");
		sb.append("Last Value:" + mFD.last_data+ "\n");
		responseView.setText(sb);
		
	}

	private void startProgressBar() {
    	progress = ProgressDialog.show(ThingSpace.this, "", "Requesting...", true);
    }
    private void stopProgressBar() {
    	progress.cancel();
    }
    
	private ThingSpace.FeedData sendRequest() {
		FeedData fd = new FeedData("", 0);
        DefaultHttpClient httpClient = new DefaultHttpClient();
        HttpGet httpGet = new HttpGet("https://thingspeak.com/channels/"+channel.getText()+"/field/1.json");
        try {
			HttpResponse response = httpClient.execute(httpGet);
			BufferedReader br = new BufferedReader(new InputStreamReader(response.getEntity().getContent()));
			JSONObject jo = new JSONObject(br.readLine());
			String name = jo.getJSONObject("channel").getString("name");
			JSONArray feeds = jo.getJSONArray("feeds");
			JSONObject last_feed = feeds.getJSONObject(feeds.length()-1); 
			double data = last_feed.getJSONObject("feed").getDouble("field1");
			fd.feedName = name;
			fd.last_data = data;
			return fd;
		} catch (ClientProtocolException e) {
			e.printStackTrace();
			return fd;
		} catch (IOException e) {
			e.printStackTrace();
			return fd;
		} catch (JSONException e) {
			e.printStackTrace();
			return fd;
		}
		
	}
}