from deepface import DeepFace
import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    try:
        result = DeepFace.represent(
            frame,
            model_name="Facenet",
            enforce_detection=False
        )
        print("Embedding extracted:", len(result[0]["embedding"]))
    except Exception as e:
        print("Error:", e)

    cv2.imshow("Test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()