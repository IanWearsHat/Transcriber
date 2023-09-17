package template_maker_gui;

import java.awt.Dimension;
import java.awt.Toolkit;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;

import javax.swing.JFrame;

public class Main {
    
    static Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
    static final int WIDTH = (int) screenSize.getWidth();
    static final int HEIGHT = (int) screenSize.getHeight();

    public static void main(String args[]) {
        JFrame frame = new JFrame();
        ClickablePanel clickablePanel = new ClickablePanel();

        frame.add(clickablePanel);
        frame.setTitle("Template Maker");
        frame.setPreferredSize(new Dimension(WIDTH, HEIGHT));
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setVisible(true);
        frame.pack();

        clickablePanel.run();

        frame.addWindowListener(new WindowAdapter() {
            public void windowClosing(WindowEvent e) {
                System.exit(0);
            }
        });

    }
}
