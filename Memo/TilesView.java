package com.example.memo;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.drawable.Drawable;
import android.os.AsyncTask;
import android.util.AttributeSet;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Toast;

import androidx.annotation.Nullable;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

class Card {
    Paint p = new Paint();
    Bitmap front;
    Bitmap back;
    int imageId;

    public Card(float x, float y, float width, float height, int imageId, Bitmap front, Bitmap back) {
        this.imageId = imageId;
        this.front = front;
        this.back = back;
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
    }

    boolean isOpen = false;
    boolean isMatch = false;
    float x, y, width, height;

    public void draw(Canvas c) {
        if (isMatch) return;

        if (isOpen) {
            c.drawBitmap(front, x, y, p);
        } else {
            c.drawBitmap(back, x, y, p);
        }
    }

    public boolean flip(float touch_x, float touch_y) {
        if (isMatch) return false;
        if (touch_x >= x && touch_x <= x + width && touch_y >= y && touch_y <= y + height) {
            isOpen = !isOpen;
            return true;
        }
        return false;
    }
}

public class TilesView extends View {
    final int PAUSE_LENGTH = 1;
    boolean isOnPauseNow = false;
    boolean notFirstDraw = false;
    int openedCard = 0;
    ArrayList<Card> cards = new ArrayList<>();
    int width, height;
    Card first = null;
    Card second = null;
    int pairsFound = 0;
    int TOTAL = 8;

    private int[] frontImages = {
            R.drawable.alien,
            R.drawable.ball,
            R.drawable.dog,
            R.drawable.flower,
            R.drawable.fox,
            R.drawable.planet,
            R.drawable.present,
            R.drawable.puzzle
    };

    public TilesView(Context context) {
        super(context);
    }

    public TilesView(Context context, @Nullable AttributeSet attrs) {
        super(context, attrs);
    }

    private void drawCards() {
        cards.clear();
        pairsFound = 0;

        List<Integer> images = new ArrayList<>();
        for (int image : frontImages) {
            images.add(image);
            images.add(image);
        }
        Collections.shuffle(images);

        int cols = 4;
        int rows = 4;

        int cWidth = 250;
        int cHeight = 300;
        int margin = 15;

        int gridWidth = cols * cWidth + (cols - 1) * margin;
        int gridHeight = rows * cHeight + (rows - 1) * margin;

        int startX = (width - gridWidth) / 2;
        int startY = (height - gridHeight) / 2;

        Bitmap back = BitmapFactory.decodeResource(getResources(), R.drawable.back_card);
        Bitmap resizeBack = Bitmap.createScaledBitmap(back, cWidth, cHeight, true);

        int ind = 0;
        for (int row = 0; row < rows; row++) {
            for (int col = 0; col < cols; col++){
                int x = startX + col * (cWidth + margin);
                int y = startY + row * (cHeight + margin);

                Bitmap front = BitmapFactory.decodeResource(getResources(), images.get(ind));
                Bitmap resizeFront = Bitmap.createScaledBitmap(front, cWidth, cHeight, true);

                Card card = new Card(x, y, cWidth, cHeight, images.get(ind), resizeFront,resizeBack );
                cards.add(card);
                ind++;
            }
        }
    }

    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);

        width = canvas.getWidth();
        height = canvas.getHeight();

        if (!notFirstDraw){
            drawCards();
            notFirstDraw = true;
        }


        for (Card c : cards) {
            c.draw(canvas);
        }

        Paint textPaint = new Paint();
        textPaint.setTextSize(80);
        canvas.drawText("Найдено пар: " + pairsFound + "/" + TOTAL, 100, 160, textPaint);
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        int x = (int) event.getX();
        int y = (int) event.getY();

        if (event.getAction() == MotionEvent.ACTION_DOWN && !isOnPauseNow) {
            for (Card c : cards) {

                if (openedCard == 0) {
                    if (c.flip(x, y)) {
                        first = c;
                        openedCard++;
                        invalidate();
                        return true;
                    }
                } else if (openedCard == 1) {
                    if (c.flip(x, y) && c != first) {
                        second = c;
                        openedCard++;

                        if (first.imageId == second.imageId) {
                            pairsFound++;

                            PauseTask1 task = new PauseTask1();
                            task.execute(PAUSE_LENGTH);
                            isOnPauseNow = true;

                            if (pairsFound == TOTAL) {
                                Toast.makeText(getContext(), "Вы выиграли!", Toast.LENGTH_SHORT).show();
                            }

                        } else {

                            PauseTask task = new PauseTask();
                            task.execute(PAUSE_LENGTH);
                            isOnPauseNow = true;
                        }
                        invalidate();
                        return true;
                    }
                }
            }
        }
        return true;
    }

    public void newGame() {

        openedCard = 0;
        first = null;
        second = null;
        pairsFound = 0;
        isOnPauseNow = false;

        drawCards();
        invalidate();
    }

    class PauseTask extends AsyncTask<Integer, Void, Void> {
        @Override
        protected Void doInBackground(Integer... integers) {
            try {
                Thread.sleep(integers[0] * 1000);
            } catch (InterruptedException e) {}
            return null;
        }

        @Override
        protected void onPostExecute(Void aVoid) {
            if (first != null) {
                first.isOpen = false;
            }
            if (second != null) {
                second.isOpen = false;
            }
            openedCard = 0;
            first = null;
            second = null;
            isOnPauseNow = false;
            invalidate();
        }
    }

    class PauseTask1 extends AsyncTask<Integer, Void, Void> {
        @Override
        protected Void doInBackground(Integer... integers) {
            try {
                Thread.sleep(integers[0] * 1000);
            } catch (InterruptedException e) {}
            return null;
        }

        @Override
        protected void onPostExecute(Void aVoid) {
            if (first != null) {
                first.isMatch = true;
            }
            if (second != null) {
                second.isMatch = true;
            }
            openedCard = 0;
            first = null;
            second = null;
            isOnPauseNow = false;
            invalidate();
        }
    }
}