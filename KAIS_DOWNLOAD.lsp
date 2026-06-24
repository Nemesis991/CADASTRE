;;; ==========================================================================
;;; ПРОФЕСИОНАЛНА АВТОМАТИЗАЦИЯ КАИС - ФАЙЛОВЕТЕ ОТИВАТ ПРИ ЧЕРТЕЖА
;;; Команда: ekate
;;; ==========================================================================

;; ---> НАСТРОЙКА: ПЪТЯТ ДО ПАПКАТА С ПРОГРАМАТА (КЪДЕТО Е Python СКРИПТЪТ) <---
(setq *KAIS_DIR* "C:\\CADSTRE\\")

(defun c:ekate ( / ss i e txt len ch i2 numStr resList f dwgDir inputPath scriptPath batPath fBat c WshShell)
  (vl-load-com)
  
  ;; 1. Вземаме папката на ТЕКУЩИЯ чертеж
  (setq dwgDir (getvar "DWGPREFIX"))
  
  ;; Застраховка: Ако чертежът е нов и не е запазен (Drawing1), ползваме главната папка
  (if (or (= dwgDir "") (not dwgDir))
    (setq dwgDir *KAIS_DIR*)
  )

  ;; 2. Текстовият файл и BAT файлът се създават директно ПРИ ЧЕРТЕЖА
  (setq inputPath (strcat dwgDir "selected_ekatte.txt"))
  (setq batPath (strcat dwgDir "run_kais.bat"))
  
  ;; 3. Пътят до самия Python скрипт остава твърдо в папката на програмата
  (setq scriptPath (strcat *KAIS_DIR* "CAD_IMPORT.py"))

  (princ "\nMarkirai tekstovete s EKATTE kodove: ")
  
  (if (setq ss (ssget '((0 . "TEXT,MTEXT"))))
    (progn
      (setq resList '())
      (repeat (setq i (sslength ss))
        (setq e (vlax-ename->vla-object (ssname ss (setq i (1- i)))))
        (setq txt (vlax-get e 'TextString))
        
        (while (vl-string-search "\\P" txt) (setq txt (vl-string-subst " " "\\P" txt)))
        (while (vl-string-search "\\p" txt) (setq txt (vl-string-subst " " "\\p" txt)))
        
        (setq len (strlen txt)) (setq numStr "") (setq i2 1)
        
        (while (<= i2 len)
          (setq ch (substr txt i2 1)) (setq c (ascii ch))
          (if (and (>= c 48) (<= c 57))
            (setq numStr (strcat numStr ch))
            (if (= (strlen numStr) 5) (setq i2 len) (if (< (strlen numStr) 5) (setq numStr "")))
          )
          (setq i2 (1+ i2))
        )
        
        (if (and (= (strlen numStr) 5) (not (member numStr resList))) 
          (setq resList (cons numStr resList))
        )
      )
      
      (if (> (length resList) 0)
        (progn
          ;; Създаване на файла с кодовете при чертежа
          (setq f (open inputPath "w"))
          (foreach item resList (write-line item f))
          (close f)
          
          ;; Създаване на BAT файла при чертежа
          (setq fBat (open batPath "w"))
          (write-line "@echo off" fBat)
          (write-line "color 0A" fBat)
          ;; Сменяме работната директория на конзолата да е тази на чертежа
          (write-line (strcat "cd /d \"" dwgDir "\"") fBat)
          ;; Извикваме Python скрипта от неговата папка
          (write-line (strcat "\"%LOCALAPPDATA%\\Programs\\Python\\Python310\\python.exe\" \"" scriptPath "\"") fBat)
          (write-line "pause" fBat)
          (close fBat)
          
          (princ (strcat "\n[i] Exportirani " (itoa (length resList)) " zemlishta. Startirane na Python..."))
          
          ;; Изпълняваме BAT файла
          (setq WshShell (vlax-create-object "WScript.Shell"))
          (vlax-invoke-method WshShell 'Run (strcat "\"" batPath "\"") 1 0)
          (vlax-release-object WshShell)
        )
        (princ "\n[X] Ne bqha otkriti 5-cifreni kodove.")
      )
    )
    (princ "\n[X] Nqma selektirani obekti.")
  )
  (princ)
)

(princ "\n*** APLIKACIQTA 'EKATE' E USPESHNO ZAREDENA! ***")
(princ)