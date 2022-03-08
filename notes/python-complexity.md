---
description: Временная сложность стандартных контейнеров в python
tags: python-standart-library
---
# Python time complexity

## List

Внутри список представлен как массив; самые большие затраты связаны с выходом за пределы текущего размера (потому что приходится сдвигать весь массив) или со вставкой или удалением где-то в начале списка (по той же причине). Если нужно добавлять/удалять с обоих концов, то лучше использовать [[deque]]

<table><tbody>
<tr>
  <td><strong>Operation</strong></td>
  <td><strong>Average Case</strong></td>
  <td><strong>Amortized Worst Case</strong></td>
</tr>
<tr>
  <td>Copy</td>
  <td>O(n)</td>
  <td>O(n)</td>
</tr>
<tr>
  <td>Append[1] </td>
  <td>O(1) </td>
  <td>O(1) </td>
</tr>
<tr>
  <td>Pop last </td>
  <td>O(1) </td>
  <td>O(1) </td>
</tr>
<tr>
  <td>Pop intermediate[2] </td>
  <td>O(n) </td>
  <td>O(n) </td>
</tr>
<tr>
  <td>Insert </td>
  <td>O(n) </td>
  <td>O(n) </td>
</tr>
<tr>
  <td>Get Item </td>
  <td>O(1) </td>
  <td>O(1) </td>
</tr>
<tr>
  <td>Set Item </td>
  <td>O(1) </td>
  <td>O(1) </td>
</tr>
<tr>
  <td>Delete Item </td>
  <td>O(n) </td>
  <td>O(n) </td>
</tr>
<tr>
  <td>Iteration </td>
  <td>O(n) </td>
  <td>O(n) </td>
</tr>
<tr>
  <td>Get Slice </td>
  <td>O(k) </td>
  <td>O(k) </td>
</tr>
<tr>
  <td>Del Slice </td>
  <td>O(n) </td>
  <td>O(n) </td>
</tr>
<tr>
  <td>Set Slice </td>
  <td>O(k+n) </td>
  <td>O(k+n) </td>
</tr>
<tr>
  <td>Extend[1] </td>
  <td>O(k) </td>
  <td>O(k) </td>
</tr>
<tr>
  <td>Sort </td>
  <td>O(n log n) </td>
  <td>O(n log n) </td>
</tr>
<tr>
  <td>Multiply </td>
  <td>O(nk) </td>
  <td>O(nk) </td>
</tr>
<tr>
  <td>x in s </td>
  <td>O(n) </td>
  <td> </td>
</tr>
<tr>
  <td>min(s), max(s) </td>
  <td>O(n) </td>
  <td> </td>
</tr>
<tr>
  <td>Get Length </td>
  <td>O(1) </td>
  <td>O(1) </td>
</tr>
<tr>
  <td>Concatenate two lists </td>
  <td>O(n + m) </td>
  <td>O(n + m) </td>
</tr>
</tbody></table>

## [[deque]]

Deque (двусторонняя очередь) внутренне представляется как двусвязный список. (список массивов, а не объектов, для большей эффективности) Оба конца доступны для операций. Поиск, выбор, добавление и удаление элементов из середины очень медленные.

<table><tbody>
<tr>
  <td><strong>Operation</strong> </td>
  <td><strong>Average Case</strong> </td>
  <td><strong>Amortized Worst Case</strong> </td>
</tr>
<tr>
  <td>Copy </td>
  <td>O(n) </td>
  <td>O(n) </td>
</tr>
<tr>
  <td>append </td>
  <td>O(1) </td>
  <td>O(1) </td>
</tr>
<tr>
  <td>appendleft </td>
  <td>O(1) </td>
  <td>O(1) </td>
</tr>
<tr>
  <td>pop </td>
  <td>O(1) </td>
  <td>O(1) </td>
</tr>
<tr>
  <td>popleft </td>
  <td>O(1) </td>
  <td>O(1) </td>
</tr>
<tr>
  <td>extend </td>
  <td>O(k) </td>
  <td>O(k) </td>
</tr>
<tr>
  <td>extendleft </td>
  <td>O(k) </td>
  <td>O(k) </td>
</tr>
<tr>
  <td>rotate </td>
  <td>O(k) </td>
  <td>O(k) </td>
</tr>
<tr>
  <td>remove </td>
  <td>O(n) </td>
  <td>O(n) </td>
</tr>
</tbody></table>

## Set

Реализация множества похожа на словарь

<table><tbody><tr>  <td><strong>Operation</strong> </td>
  <td><strong>Average case</strong> </td>
  <td><strong>Worst Case</strong> </td>
</tr>
<tr>  <td>add </td>
  <td>O(1) </td>
  <td>O(1) </td>
</tr>
<tr>  <td>del </td>
  <td>O(1) </td>
  <td>O(1) </td>
</tr>
<tr>  <td>x in s </td>
  <td>O(1) </td>
  <td>O(n) </td>
</tr>
<tr>  <td>Union s|t </td>
  <td>O(len(s)+len(t)) </td>
  <td> </td>
</tr>
<tr>  <td>Intersection s&amp;t </td>
  <td>O(min(len(s), len(t)) (replace "min" with "max" if t is not a set)</td>
  <td>O(len(s) * len(t)) </td>
</tr>
<tr>  <td>Multiple intersection s1&amp;s2&amp;..&amp;sn </td>
  <td> </td>
  <td>(n-1)*O(l) where l is max(len(s1),..,len(sn)) </td>
</tr>
<tr>  <td>Difference s-t </td>
  <td>O(len(s)) </td>
  <td> </td>
</tr>
<tr>  <td>s.difference_update(t) </td>
  <td>O(len(t)) </td>
  <td> </td>
</tr>
<tr>  <td>Symmetric Difference s^t </td>
  <td>O(len(s)) </td>
  <td>O(len(s) * len(t)) </td>
</tr>
<tr>  <td>s.symmetric_difference_update(t) </td>
  <td>O(len(t)) </td>
  <td>O(len(t) * len(s)) </td>
</tr>
</tbody></table>

Сложность s-t или s.difference(t) (set_difference()) и разницы вычисляемой на месте s.difference_update(t) (set_difference_update_internal()) различна! Первый — O(len(s)) (для каждого элемента в s добавить его в новый набор, если он не в t). Второй — O(len(t)) (для каждого элемента t удалить его из s). Таким образом, необходимо подумать о том, какой из них предпочтительнее, в зависимости от того, какой из наборов является самым длинным и нужен ли новый набор.

Для выполнения операций над множествами, таких как s-t, и s, и t должны быть множествами. Однако можно реализовать и эквивалент, даже если t является любым итерируемым объектом, например, s.difference(l), где l — список.

## Dict

Среднее время обработки, указанное для объектов dict, предполагает, что хеш-функция для объектов достаточно надежна, чтобы избежать коллизий. Средний случай предполагает, что ключи, используемые в параметрах, выбираются случайным образом из набора всех ключей.

Обратите внимание, что существует быстрый путь для словарей, который (на практике) работает только с ключами str; это не влияет на алгоритмическую сложность, но может значительно повлиять на константы: как быстро фактически завершается программа

<table><tbody><tr>  <td><strong>Operation</strong> </td>
  <td><strong>Average Case</strong> </td>
  <td><strong>Amortized Worst Case</strong> </td>
</tr>
<tr>  <td>k in d </td>
  <td>O(1) </td>
  <td>O(n) </td>
</tr>
<tr>  <td>Copy[3] </td>
  <td>O(n) </td>
  <td>O(n) </td>
</tr>
<tr>  <td>Get Item </td>
  <td>O(1) </td>
  <td>O(n) </td>
</tr>
<tr>  <td>Set Item[1] </td>
  <td>O(1) </td>
  <td>O(n) </td>
</tr>
<tr>  <td>Delete Item </td>
  <td>O(1) </td>
  <td>O(n) </td>
</tr>
<tr>  <td>Iteration[3] </td>
  <td>O(n) </td>
  <td>O(n) </td>
</tr>
</tbody></table>

[1] - Эти операции основаны на «амортизированной» части «наихудшего случая». Отдельные действия могут занять гораздо больше времени, в зависимости от истории контейнера.

[2] - Извлечение промежуточного элемента с индексом k из списка размера n смещает все элементы после k на один слот влево с помощью memmove. n - k элементов должны быть перемещены, поэтому O(n-k). В лучшем случае извлекается предпоследний элемент, что требует одного шага, в худшем случае извлекается первый элемент, для чего требуется n-1 шагов. Средний случай для среднего значения k — выталкивание элемента из середины списка, для чего требуется O(n/2) = O(n) операций.

[3] - Для этих операций наихудший случай n — это максимальный размер контейнера, когда-либо достигнутый, а не только текущий размер. Например, если в словарь добавляются N объектов, то N-1 удаляются, словарь по-прежнему будет рассчитан на N объектов (как минимум) до тех пор, пока не будет сделана другая вставка.

Смотри еще:

- [основная статья на wiki](https://wiki.python.org/moin/TimeComplexity)
- [амортизационный анализ](https://en.wikipedia.org/wiki/Amortized_analysis)
- [[python-standart-library]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[deque]: deque "Deque - двухсторонние очереди"
[deque]: deque "Deque - двухсторонние очереди"
[python-standart-library]: ../lists/python-standart-library "Стандартная библиотека python и полезные ресурсы"
[//end]: # "Autogenerated link references"