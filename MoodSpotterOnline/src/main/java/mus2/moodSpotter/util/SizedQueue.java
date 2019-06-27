package mus2.moodSpotter.util;


import java.util.LinkedList;

public class SizedQueue<T> extends LinkedList<T> {
    int maxSize;

    public SizedQueue(int maxSize){
        super();
        this.maxSize = maxSize;
    }

    @Override
    public boolean add(T item){
        if(super.size() > maxSize)
            super.pop();
        return super.add(item);
    }

}
