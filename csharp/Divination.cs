using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using TMPro;
using UnityEngine.UI;
using System.Text.RegularExpressions;

public class Divination : MonoBehaviour
{
    private char[] shiChens = new char[12];
    private char[] baGua = new char[8];
    public TMP_InputField inputField;

    public TextMeshProUGUI text1;
    public TextMeshProUGUI text2;
    public TextMeshProUGUI text3;
    public TextMeshProUGUI text4;
    public TextMeshProUGUI resultText;

    public GameObject errorTip;
    public GameObject results;

    private int inputNum;

    private int input1;
    private int input2;
    private int input3;

    private int num1;
    private int num2;
    private int num3;

    private void Start()
    {
        shiChens = new char[12] { '×Ó', '³ó', 'Òú', 'Ã®', '³½', 'ËÈ', 'Îç', 'Î´', 'Éê', 'ÓÏ', 'Îì', 'º¥' };
        baGua = new char[8] {  'À¤', 'ôÞ', '¿²', 'Ùã', 'Õð', 'Àë', '¶Ò', 'Ç¬' };
    }

    private int GetCurShiChen()
    {
        DateTime now = DateTime.Now;
        int hour = now.Hour;
        return (hour + 1) / 2 % 12;
    }

    public bool JudgeInput()
    {
        string str = inputField.text;
        if (str.Length < 3)
        {
            return false;
        }
        inputNum = int.Parse(str);
        input1 = inputNum / 100;
        input2 = inputNum % 100 / 10;
        input3 = inputNum % 10;
        return true;
    }

    public void Count()
    {
        errorTip.SetActive(false);
        results.SetActive(false);
        if (JudgeInput())
        {
            CountNum1();
            CountNum2();
            CountNum3();
            resultText.text = num1.ToString() + ' ' + num2.ToString() + ' ' + num3.ToString();
            results.SetActive(true);
        }
        else
        {
            errorTip.SetActive(true);
        }
    }

    private void CountNum1()
    {
        num1 = input1 % 8;
        string key1 = num1.ToString() + '£¬' + baGua[num1] + 'ØÔ';
        text1.text = key1;
    }

    private void CountNum2()
    {
        num2 = (input2 + input3) % 8;
        string key2 = num2.ToString() + '£¬' + baGua[num2] + 'ØÔ';
        text2.text = key2;
    }

    private void CountNum3()
    {
        int sc = GetCurShiChen();
        text3.text = shiChens[sc].ToString();
        num3 = (num1 + num2 + sc + 1) % 6;
        text4.text = num3.ToString();
    }
}
