# TurkeyBox - CoContest

## Optimal (SP_CC_T)

Rules:

- Parcel box consists of a list of lockers of different sizes, each with its own security code.
- Each customer orders a list of items. Multiple items can be stored inside a single locker, but
they have to fit given the locker’s size.
- One locker can contain only items of a single customer.1
- Each customer can be assigned multiple lockers.

## Data structure

```json
{
   "orders": [
      "order" {
         "bonus": "number",
         "price": ["int"],
         "height": ["int"]
      }
   ],
   "locker_height": ["int"]
}


```

### Snippets

```sh
python optimal.py dataset/1.ins tmp.out # to run testing solution
```