package template_maker_gui;

import java.awt.Graphics;
import java.awt.Graphics2D;

import javax.swing.JPanel;

public class ClickablePanel extends JPanel implements Runnable {
    private static final long FRAME_DELAY = 1000/60L;

    private static InvoiceDrawer invoiceDrawer = new InvoiceDrawer();

    public ClickablePanel() {

    }

    public void paintComponent(Graphics g) {
        super.paintComponent(g); // clears the screen before every draw

        Graphics2D g2d = (Graphics2D) g;
        invoiceDrawer.draw(g2d); // calls the renderer to handle rendering pixels
    }

    @Override
    public void run() {
        while (true) {
            requestFocusInWindow();
            repaint();

            try {
                Thread.sleep(FRAME_DELAY);
            } catch (InterruptedException e) {
            }
        }
    }

     
}