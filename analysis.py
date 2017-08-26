import Groupy # fromhttps://github.com/rhgrant10/Groupy
import regex
import collections
import itertools
import os
import pickle

messages = None
fname = 'blabla'
if os.path.isfile(fname):
    with open(fname, 'rb') as f:
        messages = pickle.load(f)
else:
    groups = Groupy.Group.list()
    group = None
    for group in groups:
        if 'tau' in group.name.lower():
            break # good enough
    print('Using the group {0}'.format(group.name))
    messages = group.messages()
    while messages.iolder():
        pass # the act of calling iolder will collect all messages into the messages list
    with open(fname, 'wb') as f:
        pickle.dump(messages, f)

p_shuttle = regex.compile(r'^(?=.*\bshuttle\b)(?=.*\bhold|wait\b).*$', regex.IGNORECASE)
#p_grad = regex.compile(r'^(?=.*\bGRE\b)(?=.*\bhold|wait\b).*$', regex.IGNORECASE)
p_congrats = regex.compile('congrats|congratulations', regex.IGNORECASE)
p_lol = regex.compile(r'^(?=.*\blol\b).*$', regex.IGNORECASE)
p_food = regex.compile('food|dinner|feed|eat|drink', regex.IGNORECASE)
p_mindset = regex.compile('mindset', regex.IGNORECASE)
p_efimba = regex.compile('efimba', regex.IGNORECASE)
p_lit = regex.compile('lit', regex.IGNORECASE)

text_messages = list(m for m in messages if m.text is not None)
efimba_messages = list(m for m in text_messages if p_efimba.search(m.text))
congrats_messages = list(m for m in text_messages if p_congrats.search(m.text))
shuttle_messages = list(m for m in text_messages if p_shuttle.search(m.text))
lol_messages = list(m for m in text_messages if p_lol.search(m.text))
mindset_messages = list(m for m in text_messages if p_mindset.search(m.text))
food_messages = list(m for m in text_messages if p_food.search(m.text))
lit_messages = list(m for m in text_messages if p_lit.search(m.text))

text_names = collections.Counter(m.name for m in text_messages)
efimba_names = collections.Counter(m.name for m in efimba_messages)
lit_names = collections.Counter(m.name for m in lit_messages)
mindset_names = collections.Counter(m.name for m in mindset_messages)
shuttle_names = collections.Counter(m.name for m in shuttle_messages)
lol_names = collections.Counter(m.name for m in lol_messages)
food_names = collections.Counter(m.name for m in food_messages)
liked = itertools.chain.from_iterable((u.nickname for u in m.likes()) for m in messages)
likers = collections.Counter(liked)

num_efimba=len(efimba_messages)
num_congrats=len(congrats_messages)
num_lit=len(lit_messages)
num_shuttle= len(shuttle_messages) #sum(1 for _ in hold_shuttle_messages)
num_lol = len(lol_messages)
num_food = len(food_messages)
num_mindset = len(mindset_messages)
num_messages = float(len(messages))
n = 5
name_format = '{} ({})' + ', {} ({})' * (n - 1)

print('There are {} messages in this group'.format(int(num_messages)))
print('The top {} senders: '.format(n) + name_format.format(*itertools.chain.from_iterable(text_names.most_common(n))))
print('{} messages contain the word "lol"; this is {:.3%}'.format(num_lol, num_lol / num_messages))
print('The top {} offenders: '.format(n) + name_format.format(*itertools.chain.from_iterable(lol_names.most_common(n))))
print('{} messages contain the word "mindset"; this is {:.3%}'.format(num_mindset, num_mindset / num_messages))
print('The top {} performers: '.format(n) + name_format.format(*itertools.chain.from_iterable(mindset_names.most_common(n))))
print('{} messages contain the word "lit"; this is {:.3%}'.format(num_lit, num_lit / num_messages))
print('The top {} lit peeps: '.format(n) + name_format.format(*itertools.chain.from_iterable(lit_names.most_common(n))))

print('{} messages contain the word "food|dinner|feed|eat|drink"; this is {:.3%}'.format(num_food, num_food / num_messages))
print('The top {} hungry people: '.format(n) + name_format.format(*itertools.chain.from_iterable(food_names.most_common(n))))
print('The top {} friendliest people: '.format(n) + name_format.format(*itertools.chain.from_iterable(likers.most_common(n))))
print('{} Number of efimba references'.format(num_efimba))
print('{} Number of congrats messages'.format(num_congrats))
